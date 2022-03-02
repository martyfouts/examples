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
