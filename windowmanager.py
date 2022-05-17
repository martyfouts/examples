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

# Examples of window_manager operators

from webbrowser import BaseBrowser
import bpy

#------------------------------------------------------------------------------
#
# Using the file browser
from bpy.types import Operator
from bpy.types import Panel
from bpy.props import StringProperty, CollectionProperty
from bpy_extras.io_utils import ImportHelper
from pathlib import Path

class TLA_OT_stlhandler(Operator, ImportHelper):
    """ Import an STL and do things with it"""
    bl_idname = "import.stlhandler"
    bl_label = "Process STL"
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(
        default='*.stl',
        options={'HIDDEN'}
    )

    files: CollectionProperty(type=bpy.types.PropertyGroup)

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        directory_path = Path(self.filepath).parent
        for file in self.files:
            bpy.ops.import_mesh.stl(filepath=str(directory_path / file.name))
            print(f'Do Your thing here')
        return {'FINISHED'}


#-----------------------------------------------------------------------------
# Here's what the ImportHelper class does as a mix-in:
# It adds a StringProperty named 'filepath'
# It adds an invoke function
# It adds a "check function.
#
# The invoke function calls context.window_manager.fileselect_add
# This class is the same as the above class, except it makes these things
# explicit
# https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
#
class TLA_OT_stlhandlerv2(Operator):
    """ Import an STL and do things with it"""
    bl_idname = "import.stlhandlerv2"
    bl_label = "Process STL"
    bl_options = {"REGISTER", "UNDO"}

    # This is usually obtained from the ImportHelper mixin
    # It is used by fileselect_add if it is present.
    filepath: StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    # This is used by fileselect_add if it is present.
    # It is not well documented.
    filter_glob: StringProperty(
        default='*.stl',
        options={'HIDDEN'}
    )

    # This is used by fileselect_add if it is present.
    directory: StringProperty(
        options={'HIDDEN'}
    )

    # This is used by fileselect_add if it is present.
    files: CollectionProperty(type=bpy.types.PropertyGroup)

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        directory_path = Path(self.filepath).parent
        for file in self.files:
            bpy.ops.import_mesh.stl(filepath=str(directory_path / file.name))
            print(f'Do Your thing here')
        return {'FINISHED'}

    # This is usually obtained from the ImportHelper mixin
    def invoke(self, context, _event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class TLA_PT_sidebar(Panel):
    """Display Process STL"""
    bl_label = "STL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TLA"

    def draw(self, context):
        col = self.layout.column(align=True)
        prop = col.operator(TLA_OT_stlhandler.bl_idname)
        prop = col.operator(TLA_OT_stlhandlerv2.bl_idname)
 
classes = [
    TLA_OT_stlhandler,
    TLA_OT_stlhandlerv2,
    TLA_PT_sidebar,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)