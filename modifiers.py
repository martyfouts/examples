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

# Random fragments related to modifiers.

#------------------------------------------------------------------------------
#
# answer to https://blender.stackexchange.com/questions/251574/displace-texture-and-assigning-in-python
#
# Silly version using set operators
def displace():
    bpy.ops.object.modifier_add(type='DISPLACE')
    texture_set = set(bpy.data.textures.keys())
    bpy.ops.texture.new()
    new_texture_set = set(bpy.data.textures.keys()) - texture_set
    texture_name = new_texture_set.pop()
    texture = bpy.data.textures[texture_name]
    texture.type = 'VORONOI'
    bpy.context.active_object.modifiers[-1].texture = texture

# Simplified version relying on list position
def displace():
    bpy.ops.object.modifier_add(type='DISPLACE')
    bpy.ops.texture.new()
    texture = bpy.data.textures[-1]
    texture.type = 'VORONOI'
    bpy.context.active_object.modifiers[-1].texture = texture

# Markus von Broady version avoiding bpy.ops
def displace(object):
    modifier = object.modifiers.new('', type='DISPLACE')
    modifier.texture = bpy.data.textures.new("displace_voronoi", 'VORONOI')
