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
import pathlib

#------------------------------------------------------------------------------
# How to read a json file
blender_TLD =  pathlib.Path('D:/stupi/blender')
blender_python_directory = blender_TLD / 'python'
tutorials = blender_TLD / 'tutorials'
sybren = 'Sybren A. Stüvel'
scripting = 'Scripting for Artists'
assets = 'assets.json'
asset_file_path = tutorials / sybren / scripting / assets

import json
if asset_file_path.exists():
    print(f'Reading asset file {assets}')
    with open(asset_file_path) as infile:
            link_info = json.load(infile)

#------------------------------------------------------------------------------
# Render specific frames with opengl

scene = bpy.context.scene

saved_filepath = scene.render.filepath
saved_frame = scene.frame_current

frame_start = scene.frame_start
frame_end = scene.frame_end

render_path = pathlib.Path(saved_filepath)

file_prefix = 'test'

render_frames = [0, 230, 99, 1]

for frame in render_frames:
    if frame < frame_start or frame > frame_end:
        continue
    full_file_name = str(render_path / f'{file_prefix}_{frame:#03d}.jpg')
    scene.frame_set(frame)
    scene.render.filepath = full_file_name
    bpy.ops.render.opengl(write_still=True)

scene.frame_set(saved_frame)
scene.render.filepath = saved_filepath

#-----------------------------------------------------------------------------
#
# stacking svg files
from pathlib import Path

path = Path('C:\\Users\\stupi\\Downloads\\foo')

scene = bpy.context.scene

collections = set(scene.collection.children)

offset = 0.0
delta = 0.1

for f in sorted(path.glob('*.svg')):
    print(f)
    bpy.ops.import_curve.svg(filepath=str(f))
    new_collection = set(scene.collection.children) - collections
    collections = set(scene.collection.children)
    for aCollection in new_collection:
        for object in aCollection.objects:
            object.select_set(True)
        bpy.ops.transform.translate(value=(0,0,offset))
        offset += delta
        for object in aCollection.objects:
            object.select_set(False)

#-----------------------------------------------------------------------------
#
# wrapper around an importer that invokes the file dialog and then processes
# each identified file
from bpy.types import Operator, OperatorFileListElement
from bpy.props import CollectionProperty, StringProperty
from pathlib import Path

# You could replace this with a custom property that could be set from a panel
# or otherwise arrange for it to be set by the user.
default_directory = r'c:\tmp'  # or you could just set your own name here

class TLA_OT_TestImporter(Operator):
    """Select a file with data to create a shape and process it"""
    bl_idname = "myops.import_files"
    bl_label = "Import shapes" 

    directory : StringProperty(subtype='DIR_PATH')
    files : CollectionProperty(type=OperatorFileListElement)

    # replace this function with the code that opens and processes
    # the files returned by the file browser.  It will be called once
    # for each file in the selected list.
    def my_import(self, import_file):
        print(f'processing {import_file}')
        file = import_file.open()
        # insert code to read and process file here
        file.close

    # This is, more or less, what an import helper class makes available.
    # The help message for fileselect add says
    # Opens a file selector with an operator. The string properties 'filepath',
    #'filename', 'directory' and a 'files' collection are assigned when present
    # in the operator
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        base = Path(self.directory)                
        for f in self.files:
            self.my_import(base / f.name)
        
        return {'FINISHED'}

# This menu entry will be added to File -> import as the last entry.
# The technique for setting the directory starts after the closing ')'
def TLA_menu_import(self, context):
    self.layout.operator("myops.import_files", text="Import files").directory=default_directory
