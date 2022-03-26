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
import bmesh

#------------------------------------------------------------------------------
# The basic bmesh manipulation snippet
import bmesh
import random                   # Only needed for the sample operation
from math import trunc          # Only needed for the sample operation

# Get a mesh from an object and make it a bmesh
object = bpy.context.object
if not object.mode == 'EDIT':
    bm = bmesh.new()
    bm.from_mesh(object.data)
else:
    bm = bmesh.from_edit_mesh(object.data)
    

# The next lines of code are a simple example of using bmesh
faces = bm.faces
bm.faces.ensure_lookup_table()

for face in bm.faces:
    n = trunc(random.uniform(0,5))
    face.material_index = n

# update the object's mesh from the bmesh
if not object.mode == 'EDIT':
    bm.to_mesh(object.data)
    bm.free()
else:
    bmesh.update_edit_mesh(object.data)

#------------------------------------------------------------------------------
# How to create a mesh from data, turn it into a bmesh
# and then rotate the bmesh
from mathutils import Matrix, Vector
from math import radians

verts = [(0, 0, 0), (1, 0, 0), (0, 1, 1)]
edges = [(0, 1), (1, 2), (2, 0)]
faces = [(0, 1, 2)]

mesh = bpy.data.meshes.new('aMesh')
mesh.from_pydata(verts, edges, faces)
mesh.update()

object = bpy.data.objects.new('anObject', mesh)
center = sum((Vector(b) for b in object.bound_box), Vector())
center /= 8


bpy.context.collection.objects.link(object)

bm = bmesh.new()
bm.from_mesh(mesh)

bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

# https://blender.stackexchange.com/a/93238/42221
# shows how to use any arbitrary axis:
# in the example, using the first two selected vertices
# v1, v2, *_ = (v for v in bm.verts if v.select)
# axis = (v2.co - v1.co).normalized()
# rot = Matrix.Rotation(radians(45), 4, axis)

# https://docs.blender.org/api/current/bmesh.ops.html#bmesh.ops.rotate
rotation_X = Matrix.Rotation(radians(45), 4, 'X')
bmesh.ops.rotate(bm, cent=center, matrix=rotation_X, verts=bm.verts)

rotation_Z = Matrix.Rotation(radians(180), 4, 'Z')
bmesh.ops.rotate(bm, cent=center, matrix=rotation_Z, verts=bm.verts)

bm.to_mesh(mesh)
bm.free()

#------------------------------------------------------------------------------
# select the boundary of a mesh
object = bpy.context.object
if object.mode != 'EDIT':
    bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(object.data)

bm.edges.ensure_lookup_table()

for edge in bm.edges:
    if edge.is_boundary:
        edge.select_set(True)
    else:
        edge.select_set(False)

bmesh.update_edit_mesh(object.data)

#-----------------------------------------------------------------------------
#
# Bmesh bevel selected edges
object = bpy.context.object
assert(object)
assert(object.type == "MESH")

if object.mode != "EDIT":
        bpy.ops.object.mode_set(mode="EDIT")
    
bm = bmesh.from_edit_mesh(object.data)
    
bm.edges.ensure_lookup_table()

edges = [edge for edge in bm.edges if edge.select]
bmesh.ops.bevel(bm, geom=edges, offset=.1, affect="EDGES", profile_type="CUSTOM")

bmesh.update_edit_mesh(object.data)

#-----------------------------------------------------------------------------
#
# Find all of the faces that are shared by a set of vertices.
# The idea is that there should only be one.
def find_faces(vertex_list):
    if not len(vertex_list):
        return set()
    faces = set(vertex_list[0].link_faces)
    for index in range(1, len(vertex_list)):
        faces.intersection_update(vertex_list[index].link_faces)
    return faces

#-----------------------------------------------------------------------------
#
# unwrap each face of a cube separately
def make_cube_with_material(size, x, y, z):
    bpy.ops.mesh.primitive_cube_add(size=size, enter_editmode=False, align='WORLD', location=(x, y, z))
    obj = bpy.context.active_object
    #obj.data.materials.append(random.choice(mats))
    mesh = obj.data

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.reset()

    bm = bmesh.from_edit_mesh(mesh)

    bm.edges.ensure_lookup_table()
    for edge in bm.edges:
        edge.seam = True

    bm.faces.ensure_lookup_table()
    for face in bm.faces:
        face.select_set(False)

    for face in bm.faces:
        face.material_index = 0
        face.select_set(True)
        bmesh.update_edit_mesh(mesh)
        bpy.ops.uv.unwrap()
        face.select_set(False)

    bpy.ops.object.mode_set(mode='OBJECT')

#-----------------------------------------------------------------------------
#
# Two ways to meassure edges with an example of Python assert statements
object = bpy.context.active_object
assert object, "There is no active object"
assert object.type == "MESH", "The active object is not a mesh object"
mesh = object.data
for edge in mesh.edges:
    if edge.select:
        v0 = mesh.vertices[edge.vertices[0]]
        v1 = mesh.vertices[edge.vertices[1]]
        x2 = (v0.co[0] - v1.co[0]) ** 2
        y2 = (v0.co[1] - v1.co[1]) ** 2
        z2 = (v0.co[2] - v1.co[2]) ** 2
        length = (x2+y2+z2)**.5
        print(f"length of edge {edge.index} = {length}")
        
for edge in mesh.edges:
    if edge.select:
        v0 = mesh.vertices[edge.vertices[0]]
        v1 = mesh.vertices[edge.vertices[1]]
        x2 = (v0.co[0] - v1.co[0]) ** 2
        y2 = (v0.co[1] - v1.co[1]) ** 2
        z2 = (v0.co[2] - v1.co[2]) ** 2
        length = (x2+y2+z2)**.5
        print(f"length of edge {edge.index} = {(v0.co-v1.co).length}")

#-----------------------------------------------------------------------------
#
# Using bmesh to assign random color islands to collection
import random
from math import trunc

object = bpy.context.object
if object.mode == 'OBJECT':
    bm = bmesh.new()
    bm.from_mesh(object.data)
else:
    bm = bmesh.from_edit_mesh(object.data)
    

islands = []

bm.faces.ensure_lookup_table()
bm.verts.ensure_lookup_table()

# https://github.com/Aadjou/blender-scripts/blob/master/bmesh-get-linked-faces.py
def get_linked_faces(f):
    if f.tag:
        # If the face is already tagged, return empty list
        return []
    # Add the face to list that will be returned
    f_linked = [f]
    f.tag = True
    # Select edges that link two faces
    edges = [e for e in f.edges if len(e.link_faces) == 2]
    for e in edges:
        # Select all firs-degree linked faces, that are not yet tagged
        faces = [elem for elem in e.link_faces if not elem.tag]
        # Recursively call this function on all connected faces
        if not len(faces) == 0:
            for elem in faces:
                # Extend the list with second-degree connected faces
                f_linked.extend(get_linked_faces(elem))
    return f_linked

examined = set()
islands = []

for face in bm.faces:
    face.tag = False

for face in bm.faces:
    if face in examined:
        continue
    links = get_linked_faces(face)
    for linked_face in links:
        examined.add(linked_face)
    islands.append(links)

for island in islands:
    n = trunc(random.uniform(0,5))
    for face in island:
        face.material_index = n

# update the object's mesh from the bmesh
if object.mode == 'OBJECT':
    bm.to_mesh(object.data)
    bm.free()
else:
    bmesh.update_edit_mesh(object.data)

#-----------------------------------------------------------------------------
#
# bmesh: vertex groups from faces

object = bpy.context.object

if object and object.type == 'MESH':

    # Create a bmesh from the object
    if object.mode == 'OBJECT':
        bm = bmesh.new()
        bm.from_mesh(object.data)
    else:
        bm = bmesh.from_edit_mesh(object.data)
        
    # Validate bmesh data structures
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    deform_layer = bm.verts.layers.deform.verify()

    # process each face in the bmesh
    for i, face in enumerate(bm.faces):
        group = object.vertex_groups.new(name=f'GRP_{i:02}')
        # Assign each vertex in the face to the face's vertex group
        for vert in face.verts:
            vert[deform_layer][group.index] = 1.0

    # update the object's mesh from the bmesh
    if object.mode == 'OBJECT':
        bm.to_mesh(object.data)
        bm.free()
    else:
        bmesh.update_edit_mesh(object.data)

#------------------------------------------------------------------------------
# how to determine if an edge is parallel to an axis
# this relies on the dot product of perpendicular vectors being zero
edges = bm.edges
bm.edges.ensure_lookup_table()

x = Vector((1,0,0))

edges_x = []
edges_not_x = []
for edge in edges:
    v = edge.verts[0].co - edge.verts[1].co
    xedge = v.dot(x)
    if abs(xedge) < .001:
        edges_not_x.append(edge)
    else:
        edges_x.append(edge)

#-----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/258626/python-how-to-make-a-new-object-out-of-selected-verts-via-bmesh
original = bpy.context.object
if original.mode == 'EDIT':
    bm = bmesh.from_edit_mesh(original.data)
else:
    bm = bmesh.new()
    bm.from_mesh(original.data)
    
bmCopy = bm.copy()

meshCopy = bpy.data.meshes.new('meshCopy')
objectCopy = bpy.data.objects.new('objectCopy', meshCopy)

bmCopy.to_mesh(objectCopy.data)
bmCopy.free()

bpy.context.collection.objects.link(objectCopy)