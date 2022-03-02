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

object = bpy.context.active_object

#-----------------------------------------------------------------------------
#
# accessing F-Curve data
#
# https://docs.blender.org/api/current/bpy.types.AnimData.html
animation_data = object.animation_data

# https://docs.blender.org/api/current/bpy.types.Action.html
action = animation_data.action

# https://docs.blender.org/api/current/bpy.types.ActionFCurves.html
curves = action.fcurves

# https://docs.blender.org/api/current/bpy.types.FCurve.htm
yloc = curves[1]

# https://docs.blender.org/api/current/bpy.types.FCurveKeyframePoints.html
key_frames = yloc.keyframe_points

# https://docs.blender.org/api/current/bpy.types.Keyframe.html
k0 = key_frames[0]

nk = key_frames.insert(48.0, key_frames[0].co[1])

def dup_first_keyframe(fcurve, frame_number):
    keyframes = fcurve.keyframe_points
    keyframes.insert(frame_number, keyframes[0].co[1])

object = bpy.context.active_object
yloc = object.animation_data.action.fcurves[1]

#-----------------------------------------------------------------------------
#
# Adding a modifer to an F-curve
def enable_cycles_modifiers(action):
    """ Enable the cycles modifier on all F-Curves in this action
        except those that already have modifiers, because the
        cycles modifier must be first.
    """
    for fcurve in action.fcurves:
        modifiers = fcurve.modifiers

        if not len(modifiers):
            modifier = modifiers.new('CYCLES')
            continue
        
        if modifiers[0].type == 'CYCLES':
            continue
        
        print(f'Cannot add Cycles modifier to {action.name} F-curve {fcurve.data_path}[{fcurve.array_index}]')

            
object = bpy.context.object
if object and object.animation_data:
    action = object.animation_data.action
    enable_cycles_modifiers(action)
    
scene = bpy.context.scene
scene.frame_set(scene.frame_current)

#-----------------------------------------------------------------------------
#
# Finding the object that owns an fcurve
#
visible = [] # Set of fcurves
for object in bpy.data.objects:
    if object.animation_data and object.animation_data.action and object.animation_data.action.fcurves:
        for fcurve in object.animation_data.action.fcurves:
            if fcurve in visible:
                print(f"{object.name}")

# Alternative
found = [o for o in bpy.data.objects if o.animation_data and o.animation_data.action is fcurve.id_data]