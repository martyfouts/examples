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

#------------------------------------------------------------------------------
#
# hooking empties and vertices in a mesh either by parenting the empty to the
# vertex (meaning moving the vertex moves the empty) or by adding a hook
# modifier to the mesh and making an empty the hook target but set to a vertex
# (Meaning moving the empty moves the vertex)
#
def add_empty(name, type, size, collection):
    """ Add an empty to a collection """
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = type
    empty.empty_display_size = size
    collection.objects.link(empty)
    return empty

def parent_empty(empty, object, vert, collection):
    """ parent the specified empty to the specified
        vertex of the specified object.
        Note: Parenting will move the empty to
        the vertex
    """
    empty.parent = object
    empty.parent_type = 'VERTEX'
    empty.parent_vertices = [vert.index] * 3

def hook_empty(name, empty, object, index):
    """ Create an empty, linked to the specified
        collection. Add a hook to the specified
        object hooking the specified vertex to
        the empty.
    """
    hook = object.modifiers.new(
        name=name,
        type='HOOK'
    )
    hook.object = empty
    hook.vertex_indices_set([index])

collection = bpy.data.collections["Collection"]

object = bpy.data.objects["Grid"]
    
for i in range(len(object.data.vertices)):
    vert = object.data.vertices[i]
    if vert.select:
        print(f"parenting an empty to vertex {vert.index}")
        empty = add_empty(
            f"Parented empty_{vert.index}",
            "SPHERE",
            0.1,
            collection
        )
        parent_empty(empty, object, vert, collection)
        print(f"hooking an empty to vertex {vert.index}")
        name = f"hooked empty_{vert.index}"
        empty = add_empty(
            name,
            "SPHERE",
            0.1,
            collection
        )
        empty.location=object.matrix_world @ vert.co
        bpy.context.view_layer.update()
        hook_empty(name, empty, object, vert.index)
