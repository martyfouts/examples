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
from math import radians
from mathutils import Euler
from mathutils import Vector

# Perhaps the silliest example in the set.
# Create a light and a camera
# Create a mesh and  a material
# Assign the material to the mesh
# Create an armature
# Rig the mesh to use the Armature
# Create an animation
# render it
# Other than being lazy and using bpy.ops to extrude the mesh into
# its final form, as far as I know, there are no unnecessary calls
# to bpy.ops. Everything is done with primitives where possible.

#-----------------------------------------------------------------------------
# helper print functions
def vpp(v):
    return f'[{v.x:7.3f} {v.y:7.3f} {v.z:7.3f}]'

def show_groups(mesh):
    for vertex in mesh.vertices:
        print(f'{vertex.index:3} {vpp(vertex.co)}', end='')
        for group in vertex.groups:
            print(f' ({obj.vertex_groups[group.group].name} {group.weight})', end='')
        print()

col = bpy.data.collections['Collection']

#-----------------------------------------------------------------------------
# light the scene
lamp = bpy.data.lights.new('lamp', 'AREA')
lamp.energy=1000
light = bpy.data.objects.new('light', lamp)
light.location = Vector((5.0, 0.0, 5.0))
light.rotation_euler = Euler((0.0, radians(45.0), 0.0))
col.objects.link(light)

#-----------------------------------------------------------------------------
# place a camera
front = bpy.data.cameras.new('front')
camera = bpy.data.objects.new('Front', front)
camera.location = Vector((0.0, -10.0, 2.0))
camera.rotation_euler = Euler((radians(90.0), 0.0, 0.0))
col.objects.link(camera)

#-----------------------------------------------------------------------------
# Create an object to rig
mesh = bpy.data.meshes.new("base mesh")
obj = bpy.data.objects.new("thing", mesh)
col.objects.link(obj)

# Make the mesh
# plane at the origin
verts = [(-1, -1, 0), (1, -1, 0), (-1, 1, 0), (1, 1, 0)]
edges = [(0, 1), (1, 3), (3, 2), (2, 3)]
faces = [(0, 1, 3, 2)]
mesh.from_pydata(verts, edges, faces)
mesh.update()

# Extrude it three times
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
for z in range(0,3):
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value":(0, 0, 1),
            "orient_type":'NORMAL',
            "orient_matrix":((0, -1, 0), (1, 0, -0), (0, 0, 1)),
            "orient_matrix_type":'NORMAL',
            "constraint_axis":(False, False, True),
        }
    )

bpy.ops.object.mode_set(mode='OBJECT')

#-----------------------------------------------------------------------------
# Give it a material
material = bpy.data.materials.new(name="red")
material.use_nodes = True
tree = material.node_tree
nodes = tree.nodes
bsdf = nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (1, 0, 0, 1)
material.diffuse_color = (1, 0, 0, 1)
obj.data.materials.append(material)

#-----------------------------------------------------------------------------
# create an armature
arm = bpy.data.armatures.new('arm')
rig = bpy.data.objects.new('rig', arm)
col.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')

# name, head, tail, parent or None, connect
# bone must be listed after its parent

bones = [
    ('base', (0, 0, 0), (0, 0, 1), None, False),
    ('center', (0, 0, 1), (0, 0, 2), 'base', True),
    ('top', (0, 0, 2), (0, 0, 3), 'center', True),
]
for bone in bones:
    newbone = arm.edit_bones.new(bone[0])
    newbone.head = bone[1]
    newbone.tail = bone[2]
    if bone[3]:
        newbone.parent = arm.edit_bones[bone[3]]
        if bone[4]:
            newbone.use_connect = True

bpy.ops.object.mode_set(mode='OBJECT')

#-----------------------------------------------------------------------------
# Rig the object with the armature
# add an armature modifier to the object and set it to the armature
bpy.context.view_layer.objects.active = obj
mod = obj.modifiers.new('armature', 'ARMATURE')
mod.object = rig
obj.parent = rig

for bone in arm.bones:
    obj.vertex_groups.new(name=bone.name)
    
weights = [
    ('base', [(0, 3, 1.0), (4, 7, .5)]),
    ('center', [(4, 11, .5)]),
    ('top', [(8, 11, .5), (12, 15, 1.0)])
]

for w in weights:
    group = obj.vertex_groups[w[0]]
    for t in w[1]:
        seq = list(range(t[0], t[1] + 1))
        weight = t[2]
        group.add(seq, weight, 'REPLACE')

# show_groups(mesh)

#-----------------------------------------------------------------------------
# Add a bone constraint for the fun of it.
bone = rig.pose.bones['center']
cr = bone.constraints.new('COPY_ROTATION')
cr.target = rig
cr.subtarget = "base"
cr.use_x = False
cr.use_y = False
cr.invert_z = True
cr.target_space = 'LOCAL'
cr.owner_space = 'LOCAL'

#-----------------------------------------------------------------------------
# Create an animation
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 24

bone = rig.pose.bones['base']
bone.rotation_euler = Euler((0.0, 0.0, radians(45)), 'XYZ')
bone.keyframe_insert('rotation_euler', frame=1)
bone.rotation_euler = Euler((0.0, 0.0, radians(-45)), 'XYZ')
bone.keyframe_insert('rotation_euler', frame=12)
bone.rotation_euler = Euler((0.0, 0.0, radians(45)), 'XYZ')
bone.keyframe_insert('rotation_euler', frame=24)

act = rig.animation_data.action
curve = act.fcurves[2]

#-----------------------------------------------------------------------------
# Render it
scene = bpy.data.scenes['Scene']
scene.camera = camera
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.audio_codec = 'MP3'
scene.render.engine = 'BLENDER_EEVEE'
scene.use_nodes=False
bpy.ops.render.render(animation=True, scene='Scene')

