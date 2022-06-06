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

# Some examples of preferences in the addon section. This can be a bit
# confusing, because preferences can refer to the entire preferences
# structure (https://docs.blender.org/api/current/bpy.types.Preferences.html)
# or it can refer to an addon's preferences.
# see (https://docs.blender.org/api/current/bpy.types.Addon.html#bpy.types.Addon)

# How to add a subpanel

#------------------------------------------------------------------------------

bl_info = {
    "name" : "Addon Subpanel demo",
    "description" : "A How to place a subpanel in the addon preferences",
    "author" : "Marty Fouts <fouts@fogey.com>",
    "version" : (0, 0, 1),
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

import bpy
from bpy.types import AddonPreferences
from bpy.types import Panel
from bpy.props import BoolProperty

class DemoAddonPreferences(AddonPreferences):
    bl_idname = __package__

    doPopup: BoolProperty(
        name="Display a popup",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "doPopup")

class Demo_PT_subpanel(Panel):
    bl_space_type = 'PREFERENCES'
    bl_region_type = 'WINDOW'
    bl_label="Sub panel"
    bl_parent=DemoAddonPreferences.bl_idname

    def draw(self,context):
        self.layout.label(text="Subpanel")

classes = [
    DemoAddonPreferences,
    Demo_PT_subpanel,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == '__main__':
    register()


#------------------------------------------------------------------------------
# iterate through enabled addons using addon_utils

import addon_utils
for mod in addon_utils.modules():
    print(mod.bl_info.get('name'), mod.bl_info.get('version', (-1, -1, -1)))
