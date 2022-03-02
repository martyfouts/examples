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
# various ways to access cameras

# Every camera in the current scene
scene_cameras = [object for object in bpy.context.scene.objects if object.type == 'CAMERA']

# Every selected camera in the current scene
selected_cameras = [object for object in bpy.context.selected_objects if object.type == 'CAMERA']

# scene camera
scene_camera = bpy.context.scene.camera

# move the scene camera to the current viewpoint
bpy.ops.view3d.camera_to_view()

#-----------------------------------------------------------------------------
#
# A function to move the camera along its follow path constraint
def segment(myConstraint):
    scene = bpy.context.scene
    frames = scene.frame_end - scene.frame_start + 1.
    current = scene.frame_current - scene.frame_start
    new_offset = current / frames
    myConstraint.offset = new_offset * 100.0
    
camera = bpy.data.objects['Camera']
path = bpy.data.objects['BezierCircle']
follow_path_constraint = camera.constraints['Follow Path']

bpy.context.scene.frame_current = 30
segment(follow_path_constraint)

#-----------------------------------------------------------------------------
#
# Get the list of all tracking markers
# https://blender.stackexchange.com/questions/248078/how-can-i-get-the-list-of-all-tracking-markers-using-python-command


for clip in bpy.data.movieclips:
    for track in clip.tracking.tracks:
        fn = 'data/tr_{0}_{1}.csv'.format(clip.name.split('.')[0], track.name)
        with open(fn, 'w') as f:
            frameno = 0
            while True:
                markerAtFrame = track.markers.find_frame(frameno)
                if not markerAtFrame:
                    break
                frameno += 1
                coords = markerAtFrame.co.xy
                f.write('{0} {1}n'.format(coords[0], coords[1]))