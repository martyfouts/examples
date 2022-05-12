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
# How to create an stash actions:
# https://blender.stackexchange.com/questions/254615/how-can-i-push-all-actions-into-nla-trough-blender-headless-with-python
object = bpy.context.active_object

# Function taken from https://devtalk.blender.org/t/context-override-for-action-stashing/7559
def stash(obj, action, track_name, start_frame):
    # Simulate stash :
    # * add a track
    # * add an action on track
    # * lock & mute the track
    # * remove active action from object
    tracks = obj.animation_data.nla_tracks
    new_track = tracks.new(prev=None)
    new_track.name = track_name
    strip = new_track.strips.new(action.name, start_frame, action)
    new_track.lock = True
    new_track.mute = True
    obj.animation_data.action = None

# Create an action - move the object on the y axis
object.location = (0,0,0)
object.keyframe_insert("location", frame = 1)
object.location = (0,3,0)
object.keyframe_insert("location", frame = 13)
object.animation_data.action.name = "move me"
stash(object, object.animation_data.action, 'move track', 1)

# Create another action - rotate the object on the y axis
object.rotation_euler = (0,0,0)
object.keyframe_insert("rotation_euler", frame = 1)
object.rotation_euler = (0,1,0)
object.keyframe_insert("rotation_euler", frame = 13)
object.animation_data.action.name = "turn me"
stash(object, object.animation_data.action, 'turn track', 1)

#------------------------------------------------------------------------------
# https://blender.stackexchange.com/questions/255423/move-strips-and-add-transition-in-nla-editor-using-python
# Move strips between tracks in the NLA

# Assume we want to deal with actions associated with the active object
object = bpy.context.active_object
tracks = object.animation_data.nla_tracks

# For a different set up, replace "NlaTrack.002" with the name of the destination track
dst_track = tracks["NlaTrack.002"]

# For a different set up, replace "NlaTrack.001" with the name of the source track.
src_track = tracks["NlaTrack.001"]

# Assume that the strip to be moved is the first strip on the track.
# We could, instead, simply select an action from bpy.data.actions and not bother
# with an additional strip
src_strip = src_track.strips[0]

# We really need the action, not the strip
action = src_strip.action

# Since we are "moving" the strip, we delete it from the src track
src_track.strips.remove(src_strip)

# The 2nd argument is the frame number where the action goes. It has to be an integer.
# We assume that it goes adjacent to the last strip already on the track.
new_strip = dst_track.strips.new(action.name, int(dst_track.strips[-1].frame_end+1), action)

# Now you can use new_strip to set transition or add modifiers.  See the manual entry
# https://docs.blender.org/api/current/bpy.types.NlaStrips.htm for details on the fields
# for instance
# new_strip.blend_in = SOME_FRAME_NUMBER


# This is unnecessary for just "moving" a strip.  Here only for completeness.
tracks.remove(src_track)

# This is just a repeat of the above, but applied to a different track.
src_track = tracks["NlaTrack"]
src_strip = src_track.strips[0]
action = src_strip.action
src_track.strips.remove(src_strip)
new_strip = dst_track.strips.new(action.name, int(dst_track.strips[-1].frame_end+1), action)
tracks.remove(src_track)

#------------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/262783/how-to-delete-a-keyframe-of-an-object-at-a-specific-frame-with-python
#
# oops, this deletes all of the animation data, but the OP only wanted a specific frame.
bpy.context.scene.frame_current = 1
object = bpy.context.active_object
animation_data = object.animation_data

if animation_data.action:
    print(f"{object.name} has an action {animation_data.action.name}")
    bpy.data.actions.remove(animation_data.action)
    
for track in animation_data.nla_tracks:
    print(f"{object.name} has an nla track {track.name}")
    for strip in track.strips:
        print(f"{track.name} has a strip {strip.name} with action {strip.action.name}")
        bpy.data.actions.remove(strip.action)
    animation_data.nla_tracks.remove(track)

# This version does what the OP asked and removes only specific keyframes
def remove_keyframes(object, action, frame_number):
    for curve in action.fcurves:
        object.keyframe_delete(data_path=curve.data_path, frame=frame_number)

def delete_all_keyframes(object, frame_number):
    animation_data = object.animation_data
    if animation_data.action:
        remove_keyframes(object, animation_data.action, frame_number)
    for track in animation_data.nla_tracks:
        for strip in track.strips:
            remove_keyframes(object, strip.action, frame_number)

#------------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/263420/create-nla-transition-with-python
#
# Add a transition between two NLA strips
# Generate an override that can be used for this call.
win = bpy.context.window
scr = win.screen
areas  = [area for area in scr.areas if area.type == 'NLA_EDITOR']
regions   = [region for region in areas[0].regions if region.type == 'WINDOW']
override = { 'area': areas[0], 'region' : regions[0] }

# Replace this line with one that selects the object that has the NLA Tracks
object = bpy.context.active_object

# Replace this line with one that selects the NLA Track you want.
track = object.animation_data.nla_tracks['NlaTrack']

# Replace the next two lines with ones that select the desired strips.
# They must be adjacent.
# No other strips should be selected so you may have to deselect all first.
track.strips[0].select = True
track.strips[1].select = True

# Add the transition, using the override calculated earlier.
bpy.ops.nla.transition_add(override)


#------------------------------------------------------------------------------
#
# Somewhat harder: copy a track
# https://blender.stackexchange.com/questions/263420/create-nla-transition-with-python
#
# copy an NLA strip to another track
# Generate an override that can be used for this call.
win = bpy.context.window
scr = win.screen
areas  = [area for area in scr.areas if area.type == 'NLA_EDITOR']
regions   = [region for region in areas[0].regions if region.type == 'WINDOW']
override = { 'area': areas[0], 'region' : regions[0] }

# Replace this line with one that selects the object that has the NLA Tracks
object = bpy.context.active_object

# Replace this line with one that selects the NLA Track you want.
src_track = object.animation_data.nla_tracks['NlaTrack']

dst_track =  object.animation_data.nla_tracks.new()
dst_track.name = 'copy'

# https://blender.stackexchange.com/questions/74183/how-can-i-copy-nla-tracks-from-one-armature-to-another
# heavily adapted

def strip_fill_action(newstrip, strip):
    newstrip.name = strip.name
    newstrip.frame_start = strip.frame_start
    newstrip.frame_end = strip.frame_end 
    newstrip.extrapolation = strip.extrapolation
    newstrip.blend_type = strip.blend_type
    newstrip.use_auto_blend = strip.use_auto_blend       
    newstrip.blend_in = strip.blend_in
    newstrip.blend_out= strip.blend_out            
    newstrip.mute = strip.mute
    newstrip.use_reverse = strip.use_reverse
    newstrip.action_frame_start = strip.action_frame_start
    newstrip.action_frame_end = strip.action_frame_end
    newstrip.scale = strip.scale
    newstrip.repeat = strip.repeat 
    newstrip.use_animated_influence = strip.use_animated_influence
    newstrip.influence = strip.influence            
    newstrip.use_animated_time = strip.use_animated_time
    newstrip.use_animated_time_cyclic = strip.use_animated_time_cyclic
    newstrip.strip_time = strip.strip_time

# Copy the action (CLIP) strips, remembering where there are transitions.
transitions = list()
for index, strip in enumerate(src_track.strips):
    if strip.type == 'TRANSITION':
        transitions.append(index)
    elif strip.type == 'CLIP':
        newstrip = dst_track.strips.new(strip.name, 
                            int(strip.frame_start), strip.action)
        strip_fill_action(newstrip, strip)
    else:
        print(f"Unsupported type {strip.type} at {index}")

# Insert any transitions that were found.
for index in transitions:
    dst_track.strips[index-1].select = True
    dst_track.strips[index].select = True
    bpy.ops.nla.transition_add(override)
    dst_track.strips[index-1].select = False
    dst_track.strips[index].select = False
   
