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

#----------------------------------------------------------------------------
#
# Basic example.  add a GN modifier, add a new node
# ad add the new node to the node tree
bpy.ops.curve.primitive_bezier_curve_add()
bpy.ops.object.modifier_add(type='NODES')

curve = bpy.context.active_object
node_group = curve.modifiers['GeometryNodes'].node_group
nodes = node_group.nodes

geom_in = nodes.get('Group Input')
geom_out = nodes.get('Group Output')

points = nodes.new('GeometryNodeMeshToPoints')

node_group.links.new(geom_in.outputs['Geometry'], points.inputs['Mesh'])
node_group.links.new(points.outputs['Points'], geom_out.inputs['Geometry'])

#----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/255417/create-an-object-with-a-geometry-node-modifier-via-script
# Create an object, give it a GN modifier, but substitute a different
# existing node tree for the default.
# 1) Create the object
# Replace this with code that creates the object you want.
bpy.ops.mesh.primitive_monkey_add()

# The op makes the object the active object. So use it
object = bpy.context.active_object

# 2) Add the GeometryNodes Modifier
modifier = object.modifiers.new("GN Test", "NODES")

# Locate the node tree you want to add to the modifier
# Replace this with code to find the node tree you want to use
replacement = bpy.data.node_groups["replacement"]

# 3) Replace the modifier's node group with the replacement
modifier.node_group = replacement

#----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/256401/how-do-i-change-font-of-string-to-curves-geometry-node-using-blender-python
# Using Ariel Black as an example.
obj = bpy.context.active_object
modifier = obj.modifiers["GeometryNodes"]
node_group = modifier.node_group
node = node_group.nodes['String to Curves']
data_font = bpy.data.fonts.load('C:\\WINDOWS\\Fonts\\ariblk.ttf')
node.font = data_font
node.font

#----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/259984/add-geometry-nodes-string-input-via-python-script
obj = bpy.context.active_object
node_group = obj.modifiers['GeometryNodes'].node_group
nodes = node_group.nodes

geom_out = nodes.get('Group Output')

string = nodes.new('FunctionNodeInputString')

node_group.links.new(string.outputs['String'], geom_out.inputs[-1])

#----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/249763/python-geometry-node-trees/249779#249779

from mathutils import Vector
bpy.ops.curve.primitive_bezier_curve_add()
bpy.ops.object.modifier_add(type='NODES')  

curve = bpy.context.active_object

def new_GeometryNodes_group():
    ''' Create a new empty node group that can be used
        in a GeometryNodes modifier.
    '''
    node_group = bpy.data.node_groups.new('GeometryNodes', 'GeometryNodeTree')
    inNode = node_group.nodes.new('NodeGroupInput')
    inNode.outputs.new('NodeSocketGeometry', 'Geometry')
    outNode = node_group.nodes.new('NodeGroupOutput')
    outNode.inputs.new('NodeSocketGeometry', 'Geometry')
    node_group.links.new(inNode.outputs['Geometry'], outNode.inputs['Geometry'])
    inNode.location = Vector((-1.5*inNode.width, 0))
    outNode.location = Vector((1.5*outNode.width, 0))
    return node_group

# In 3.2 Adding the modifier no longer automatically creates a node group.
# This test could be done with versioning, but this approach is more general
# in case a later version of Blender goes back to including a node group.
if curve.modifiers[-1].node_group:
    node_group = curve.modifiers[-1].node_group    
else:
    node_group = new_GeometryNodes_group()
    curve.modifiers[-1].node_group = node_group

nodes = node_group.nodes
