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