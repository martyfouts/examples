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