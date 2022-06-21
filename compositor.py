# Copyright 2022 Martin Fouts
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# 

import bpy

#------------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/260176/how-to-add-mist-to-an-image-programmatically
# How to enable and use the mist pass
#
scene = bpy.context.scene
scene.view_layers["ViewLayer"].use_pass_mist = True
scene.use_nodes = True

nodes = scene.node_tree.nodes

mist = bpy.data.worlds[scene.world.name].mist_settings
mist.use_mist = True
mist.intensity = 1
mist.depth = 1
mist.start = 0

#viewer_node = nodes.new('CompositorNodeViewer')
compositor_node = nodes.get('Composite')
render_layer_node = nodes.get('Render Layers')
mix_rgb_node = nodes.new('CompositorNodeMixRGB')

scene.node_tree.links.new(render_layer_node.outputs["Image"], mix_rgb_node.inputs["Image"])
scene.node_tree.links.new(render_layer_node.outputs["Mist"], mix_rgb_node.inputs["Fac"])

scene.node_tree.links.new(mix_rgb_node.outputs["Image"], compositor_node.inputs["Image"])

#------------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/267066/call-a-group-of-compositing-nodes-and-automatically-connect-them-to-the-render-l
# https://docs.blender.org/api/current/bpy.types.NodeTree.html
# https://docs.blender.org/api/current/bpy.types.CompositorNodeTree.html

# The type of a node is its bl_idname
# Render = 'CompositorNodeRLayers'
# Composite = 'CompositorNodeComposite'
# Denoise = 'CompositorNodeDenoise'
# Group = 'CompositorNodeGroup'
# Viewer = 'CompositorNodeViewer'

def find_node(tree, name, type):
    ''' return an existing node with the given name.
        If a node by that name does not exist, create a
        node of the specified type, give it the name
        and return it.
    '''
    try:
        node = tree.nodes[name]
    except KeyError:
        node = tree.nodes.new(type)
        node.name = name
    return node

def find_node_group(tree, name):
    ''' Find the first node tree with the given group name.
        Return None if there isn't one.
        Then check to see if a NodeGroup node using that node tree
        exists.  If it does return it.
        If one doesn't exist, create a new NodeGroup node and
        sets it to that node group.
    '''
    try:
        node_tree = bpy.data.node_groups[name]
    except KeyError:
        return None
    for node in tree.nodes:
        if (node.bl_idname == 'CompositorNodeGroup'
            and node.node_tree
            and node.node_tree.name == name):
            return node
    node = tree.nodes.new('CompositorNodeGroup')
    node.node_tree = node_tree
    return node
            
def insert_node(tree, original_output_socket, new_input_socket, new_output_socket):
    ''' Insert the node represented by new_input_socket an new_output_socket
        between the node represented by original_output_socket and any sockets
        that original_output_socket was connected to
    '''
    sockets =  [link.to_socket for link in original_output_socket.links]
    tree.links.new(original_output_socket, new_input_socket)
    for socket in sockets:
        tree.links.new(new_output_socket, socket)

def attach_sockets(tree, from_node, to_node, socket_list):
    ''' socket_list is alist of tuples of socket names.
        The first is the output socket of from_node to use.
        The second is the input socket of to_node.
        Each pair is linked.
        No error handling is done.
    '''
    for sockets in socket_list:
        src = from_node.outputs[sockets[0]]
        dst = to_node.inputs[sockets[1]]
        tree.links.new(src, dst)

bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

# For demonstration purposes enumerate the expected nodes
# In the demo, there isn't a Denoise node, so one will be created

render_node = find_node(tree, 'Render Layers', 'CompositorNodeRLayers')
composite_node = find_node(tree, 'Composite', 'CompositorNodeComposite')
viewer_node = find_node(tree, 'Viewer', 'CompositorNodeViewer')
# denoise_node = find_node(tree, 'Denoise', 'CompositorNodeDenoise')

# In the demo there isn't a NodeGroup node for NodeGroup so this will add one.
group_node = find_node_group(tree, 'NodeGroup')

# Insert the Denoise node after the Render Layers node.
output_socket = render_node.outputs['Image']
input_socket = group_node.inputs['Image']
new_output = group_node.outputs['Image']
insert_node(tree, output_socket, input_socket, new_output)

# A list of tuples containing the names of the output socket
# and input socket for a set of attachments.
socket_list = [
    ('Image', 'Image'),
    ('Denoising Normal', 'Normal'),
    ('Denoising Albedo', 'Albedo'),
]

attach_sockets(tree, render_node, group_node, socket_list)

# Example of creating a Node Group for the compositor
# Group Input is simply 'NodeGroupInput'
# Group Output is simply 'NodeGroupOutput'
# Denoiser is 'CompositorNodeDenoise'
# We reuse tree and render_node from above

groupnode = tree.nodes.new('CompositorNodeGroup')
newGroup = bpy.data.node_groups.new('DenoiseGroup', 'CompositorNodeTree')
groupnode.node_tree = newGroup

inNode = newGroup.nodes.new('NodeGroupInput')
outNode = newGroup.nodes.new('NodeGroupOutput')
denoiseNode = newGroup.nodes.new('CompositorNodeDenoise')

newGroup.links.new(inNode.outputs[0], denoiseNode.inputs['Image'])
newGroup.links.new(inNode.outputs[1], denoiseNode.inputs['Normal'])
newGroup.links.new(inNode.outputs[2], denoiseNode.inputs['Albedo'])
newGroup.links.new(denoiseNode.outputs['Image'], outNode.inputs[0])

output_socket = render_node.outputs['Image']
input_socket = groupnode.inputs['Image']
new_output = groupnode.outputs['Image']
insert_node(tree, output_socket, input_socket, new_output)

# A list of tuples containing the names of the output socket
# and input socket for a set of attachments.
socket_list = [
    ('Image', 'Image'),
    ('Denoising Normal', 'Normal'),
    ('Denoising Albedo', 'Albedo'),
]

attach_sockets(tree, render_node, groupnode, socket_list)