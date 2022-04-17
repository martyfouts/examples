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

# Very small add on to start from

bl_info = {
    "name" : "draw colors",
    "description" : "A skeleton addon",
    "author" : "Marty",
    "version" : (0, 0, 1),
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

import bpy
from bpy.types import Operator
from bpy.types import Panel

class TLA_OT_operator(Operator):
    """ tooltip goes here """
    bl_idname = "demo.operator"
    bl_label = "I'm a Skeleton Operator"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):

        self.report({'INFO'},
            f"execute()")

        return {'FINISHED'}


class TLA_PT_sidebar(Panel):
    """Display test button"""
    bl_label = "Closet"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TLA"

    def draw(self, context):
        col = self.layout.column(align=True)
        prop = col.operator(TLA_OT_operator.bl_idname, text="Say Something")

 
classes = [
    TLA_OT_operator,
    TLA_PT_sidebar,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()