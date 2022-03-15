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

#-----------------------------------------------------------------------------
# list all of the materials in an object;
# set all of the material slots from a list
#
material_list = []
for slot in object.material_slots:
    material_list.append(slot.material) 
    
for index, slot in enumerate(object.material_slots):
    slot.material = material_list[index]

#------------------------------------------------------------------------------
# How to find the nodes of a specific type in a material:
def find_nodes_by_type(material, node_type):
    """ Return a list of all of the nodes in the material
        that match the node type.
        Return an empty list if the material doesn't use
        nodes or doesn't have a tree.
    """
    node_list = []
    if material.use_nodes and material.node_tree:
            for n in material.node_tree.nodes:
                if n.type == node_type:
                    node_list.append(n)
    return node_list

#------------------------------------------------------------------------------
# display all of the material using objects in a scene and the materials they use
material_set = set()
for object in bpy.context.scene.objects:
    for material in object.material_slots:
        material_set.add(material)
        
for material in material_set:
    print(material.name)

#-----------------------------------------------------------------------------
#
# file names of linked materials
# also example of using namedtuple
from collections import namedtuple

Row = namedtuple("row", ['object', 'material', 'file'])

def find_linked_materials(wanted_name):
    """ returns a list of (object, material, linked file) tuples for every material
        that matches the wanted name and comes from a library
    """
    linked_materials = []

    for obj in bpy.context.scene.objects:
         for slot in obj.material_slots:
            mat = slot.material
            if mat.name == wanted_name and mat.library:
                row = Row(obj.name, wanted_name, mat.library.name)
                linked_materials.append(row)
    return linked_materials

if __name__ == '__main__':
    wanted_name = 'Carpaint Modified'
    l = find_linked_materials(wanted_name)
    for e in l:
        print(f'object {e.object} contains material {e.material} from file {e.file}')
#        print(f'object {e[0]} contains material {e[1]} from file {e[2]}')
#        print('object %s contains material %s from file %s' % e)
#        print('object {0} contains material {1} from file {2}'.e)

#-----------------------------------------------------------------------------
#
# Adding an image texture to a material and filling it with a movie

object = bpy.context.active_object
assert object
assert object.type == 'MESH'
assert len(object.material_slots) == 0

material = bpy.data.materials.new(name="FIRE")
object.data.materials.append(material)
material.use_nodes = True
tree = material.node_tree
nodes = tree.nodes

texcord = nodes.new('ShaderNodeTexCoord')
mapping = nodes.new('ShaderNodeMapping')
teximage = nodes.new("ShaderNodeTexImage")

bsdf = nodes["Principled BSDF"]
assert bsdf.type == "BSDF_PRINCIPLED"

tree.links.new(texcord.outputs[2], mapping.inputs[0])
tree.links.new(mapping.outputs[0], teximage.inputs[0])
tree.links.new(teximage.outputs[0], bsdf.inputs[0])

teximage.image = bpy.data.images["fire.mp4"]

#-----------------------------------------------------------------------------
#
# Seriously messing with materials node tree

def link_alpha(material):
    """ Find at least one image texture in the material
        and at least one Principled shader.
        If they both exist and neither have a link to
        the relevant alpha socket, connect them.
        There are many ways this can fail.
        if there's no image; if there's no principled
        shader; if the selected image/principled sockets
        are already in use.
        Returns false on any detected error.
        Does not try alternatives if there are multiple
        images or multiple principled shaders.
    """
    print(f'processing material {material.name}')
    it_list = find_nodes_by_type(material, 'TEX_IMAGE')
    if len(it_list) == 0:
        print(f'{material.name}: no image texture nodes.')
        return False
    if len(it_list) > 1:
        print(f'{material.name}: too many image textures. Trying the first one')
    s_list = find_nodes_by_type(material, 'BSDF_PRINCIPLED')
    if len(s_list) == 0:
        print(f'{material.name}: no principled shader.')
        return False
    if len(s_list) != 1:
        print(f'{material.name}: too many principled shaders. Trying the first one')
    image_node = it_list[0]
    shader_node = s_list[0]
    print(f'{material.name}: Attempting to connect {image_node.name} alpha to {shader_node.name}')
    image_socket = image_node.outputs['Alpha']
    if not image_socket:
        print(f'{material.name}: Image texture does not have an alpha node.  Something is seriously broken.')
        return False
    if image_socket.is_linked:
        print(f'{material.name}: Image texture alpha output already in use.')
        return False
    shader_socket = shader_node.inputs['Alpha']
    if not shader_socket:
        print(f'{material.name}: Principled BSDF does not have an alpha node. Version of Blender too old?')
        return False
    if shader_socket.is_linked:
        print(f'{material.name}: Principled BSDF alpha input already in use.')
        return False
    material.node_tree.links.new(shader_socket, image_socket)
    return True

#-----------------------------------------------------------------------------
#
# Print all image Texture

material_set = set()

for object in bpy.context.scene.objects:
    for material in object.material_slots:
        image_nodes = find_nodes_by_type(material.material, "TEX_IMAGE")
        if len(image_nodes):
            material_set.add(material)
        
for object in bpy.context.scene.objects:
    for material in object.material_slots:
        if material in material_set:
            print(f"Object {object.name}, uses material {material.name}")
            image_nodes = find_nodes_by_type(material.material, "TEX_IMAGE")    
            for image_node in image_nodes:
                if image_node.image:
                    print(f"\timage {image_node.image.name} has file '{image_node.image.filepath}'")
                else:
                    print("\tEmpty image texture")

#-----------------------------------------------------------------------------
#
# adding a color ramp node
activeObject = bpy.context.active_object
    
mat_ruby = bpy.data.materials.new(name="Ruby")

mat_ruby.use_nodes = True

activeObject.data.materials.append(mat_ruby)

ramp = mat_ruby.node_tree.nodes.new("ShaderNodeValToRGB")
ramp.location = (-800,100)

ramp_colors = [(0.215861,0,0.017642,1), (0.396755,0,0.032,1), (0.701102,0.147,0.016,1), (1.0,0.292,0.0,1)]
ramp_positions = [0.102, 0.636, 0.794, 0.893]

elements = ramp.color_ramp.elements
for i in range(len(ramp_colors)):
    element = elements.new(ramp_positions[i])
    element.color = ramp_colors[i]

#-----------------------------------------------------------------------------
#
# not really materials but where else to put it?
# set or toggle the object's shading mode
# https://blender.stackexchange.com/questions/248476/python-how-to-toggle-smooth-shading-in-a-script/248496#248496
def set_shading(object, OnOff=True):
    """ Set the shading mode of an object
        True means turn smooth shading on.
        False means turn smooth shading off.
    """
    if not object:
        return
    if not object.type == 'MESH':
        return
    if not object.data:
        return
    polygons = object.data.polygons
    polygons.foreach_set('use_smooth',  [OnOff] * len(polygons))
    object.data.update()

def toggle_shading(object):
    """ Toggle the shading mode of an object """
    if not object:
        return
    if not object.type == 'MESH':
        return
    if not object.data:
        return
    polygons = object.data.polygons
    for polygon in polygons:
        polygon.use_smooth = not polygon.use_smooth
    object.data.update()

#-----------------------------------------------------------------------------
#
# crude script to change all of the image textures that have png files to
# instead use dds files of the same name.
path_to_dds_files = 'C:\\users\\stupi\\downloads\\'

for material in bpy.data.materials:
    texture_nodes = find_nodes_by_type(material, 'TEX_IMAGE')
    for texture in texture_nodes:
        if texture.image.name.endswith('.png'):
            new_name = texture.image.name.split(sep='.')[-2] + '.dds'
            new_image = bpy.data.images.load(filepath = path_to_dds_files + new_name)
            print(f"{material.name}: {texture.image.name}, {new_name}")
            texture.image.name = new_image

#-----------------------------------------------------------------------------
#
# Keyframe the default value of a node
object = bpy.context.active_object
material = object.active_material
nodes = material.node_tree.nodes
node = nodes["Combine RGB"]
node.inputs[0].default_value = 0.17
node.inputs[0].keyframe_insert('default_value', frame = 42)

#-----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/5387/how-to-handle-creating-a-node-group-in-a-script
# Example of creating a node group (but not adding it to a material!)
# create a group
test_group = bpy.data.node_groups.new('testGroup', 'ShaderNodeTree')

# create group inputs
group_inputs = test_group.nodes.new('NodeGroupInput')
group_inputs.location = (-350,0)
test_group.inputs.new('NodeSocketFloat','in_to_greater')
test_group.inputs.new('NodeSocketFloat','in_to_less')

# create group outputs
group_outputs = test_group.nodes.new('NodeGroupOutput')
group_outputs.location = (300,0)
test_group.outputs.new('NodeSocketFloat','out_result')

# create three math nodes in a group
node_add = test_group.nodes.new('ShaderNodeMath')
node_add.operation = 'ADD'
node_add.location = (100,0)

node_greater = test_group.nodes.new('ShaderNodeMath')
node_greater.operation = 'GREATER_THAN'
node_greater.label = 'greater'
node_greater.location = (-100,100)

node_less = test_group.nodes.new('ShaderNodeMath')
node_less.operation = 'LESS_THAN'
node_less.label = 'less'
node_less.location = (-100,-100)

# link nodes together
test_group.links.new(node_add.inputs[0], node_greater.outputs[0])
test_group.links.new(node_add.inputs[1], node_less.outputs[0])

# link inputs
test_group.links.new(group_inputs.outputs['in_to_greater'], node_greater.inputs[0])
test_group.links.new(group_inputs.outputs['in_to_less'], node_less.inputs[0])

#link output
test_group.links.new(node_add.outputs[0], group_outputs.inputs['out_result'])

#-----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/256447/is-their-a-way-to-merge-multiple-blend-files
# This assumes that you really want every material and that you wont get 
# any errors.
# It contains both an example of linking materials (what happens in the with)
# and of appending them (what happens in the call to wm.append)
# It need error handling around the load.

import bpy
from pathlib import Path

blendfilespath = Path("d:/stupi/blender/blends/materials samples")

for file in blendfilespath.glob("*.blend") :
    file_path = Path(file)
    inner_path = "Materials"
    with bpy.data.libraries.load(str(file_path)) as (data_from, data_to):
        data_to.materials = data_from.materials
    for linked_material in data_to.materials:
        object_name = linked_material.name
        bpy.ops.wm.append(
        filepath=str(file_path / inner_path / object_name),
        directory=str(file_path / inner_path),
        filename=object_name
    )

