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
from bpy.types import Menu, Operator

#------------------------------------------------------------------------------
#
# Pie Menu Example - a pie menu to change the alignment of newly created
# Objects, written as an answer for this Stack Exchange question:
# https://blender.stackexchange.com/questions/250262/how-do-i-change-viewport-alignment-of-newly-created-objects-with-a-python-comman

# https://docs.blender.org/api/current/bpy.types.Menu.html

#------------------------------------------------------------------------------
#
# The operator to set the alignment.
# This uses an attribute to identify which menu entry was called
# So only one function is needed.
class MY_OT_align(Operator):
    bl_idname = "my.align"
    bl_label = 'Align'
    bl_description = "Set New object alignment"
    
    alignment : bpy.props.StringProperty(name="alignment", default="None")

    def execute(self, context):
         bpy.context.preferences.edit.object_align = self.alignment
         return {'FINISHED'}

# The only difference between a Pie Menu and a standard menu is that the pie
# menu uses the menu_pie layout function.
# https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.menu_pie
class MY_MT_align(Menu):
    """ A Pie Menu meant to support changing the new object orientation
    """
    bl_label = 'Align Mode'
    bl_idname = 'MY_MT_Align'

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # Each operator becomes one of the menu items in the
        # pie.  The number of items sets the pie's layout.
        # The order of items is the order of the final menu:
        # West East South North Northwest Northeast Northwest Northeast
        # More than 8 entries breaks the layout.
        # If you want a blank space in a position, but a separator there.
        pie.operator("my.align", text="World", icon = "WORLD").alignment = "WORLD"
        pie.operator("my.align", text="View", icon = "VIEW3D").alignment = "VIEW"
        pie.operator("my.align", text="Cursor", icon = "CURSOR").alignment = "CURSOR"

classes = [
    MY_OT_align,
    MY_MT_align,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
    # Since we've made no arrangement to call them menu through a
    # shortcut or an operator, we call it here as a test.
    bpy.ops.wm.call_menu_pie(name = 'MY_MT_Align')
