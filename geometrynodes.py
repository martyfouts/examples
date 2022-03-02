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
