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

# https://docs.blender.org/api/current/bpy.types.Armature.html

#------------------------------------------------------------------------------
# link an object to an armature
myObject = bpy.context.scene.objects['Cube']  # Replace with statement
                                                # to select object
myArmature =  bpy.context.scene.objects['Armature'] # Replace with statement
                                                # to select the correct armature

# Assumes that nothing else is selected at the moment
# Ignores the parentage of myObject (should verify it doesn't already have an
# armature as a parent
myObject.select_set(True)  # Must select the object first
myArmature.select_set(True) # Then select the armature
bpy.ops.object.parent_set(type='ARMATURE_AUTO') # then parent

#-----------------------------------------------------------------------------
#
# How to access the IK constraints in a rig
rig = bpy.context.scene.objects['rig']
            
for bone in rig.pose.bones:
    for constraint in bone.constraints:
        if constraint.type =='IK':
            print(f"{bone.name}: {constraint.subtarget}")

#-----------------------------------------------------------------------------
#
# The magic needed to enable Rigify. It's an addon but it's special
import addon_utils

for addon in bpy.context.preferences.addons:
    print(addon.module)

for module in addon_utils.modules():
    print(module.bl_info.get('name'))
    
addon = bpy.context.preferences.addons.get('rigify')

if not addon:
    for module in addon_utils.modules():
        if module.bl_info.get('name') == 'Rigify':
            print(module)
            addon_utils.enable(module.__name__, default_set = True)
            
# https://blender.stackexchange.com/questions/242762/how-do-i-write-a-python-script-to-enable-the-rigify-add-on-given-this-failure-i
# Turns out all you have to do is enable/disable with default_set = True
#
# So the actual code would be:

def enable_rigify():
    if not bpy.context.preferences.addons.get('rigify'):
        addon_utils.enable('rigify', default_set = True)
        
def disable_rigify():
    if bpy.context.preferences.addons.get('rigify'):
        addon_utils.disable('rigify', default_set = True)

#-----------------------------------------------------------------------------
#
# Get the edit position of a bone from an armature that is not selected
# https://docs.blender.org/api/current/bpy.types.Bone.html#bpy.types.Bone
def vformat(v):
    """ pretty print a 3 element vector """
    return f"({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f})"

armature = bpy.data.armatures['Armature']
bone = armature.bones['Bone']

# https://docs.blender.org/api/current/bpy.types.Bone.html#bpy.types.Bone
head = bone.head # relative to the parent bone
tail = bone.tail
head_local = bone.head # relative to the armature
tail_local = bone.tail
head_world = object.matrix_world @ head_local
tail_world = object.matrix_world @ tail_local

print(f"bone: {bone.name}")
print(f"      parent relative: {vformat(head)}, {vformat(tail)}")
print(f"    armature relative: {vformat(head_local)}, {vformat(tail_local)}")
print(f"       world relative: {vformat(head_world)}, {vformat(tail_world)}")

#-----------------------------------------------------------------------------
#
# Parenting is done with edit bones:
armature = bpy.data.armatures["Armature"]
if bpy.context.mode != 'EDIT_ARMATURE':
    bpy.ops.object.mode_set(mode='EDIT')
parent = armature.edit_bones["parent"]
child = armature.edit_bones["child"]
child.use_connect = True