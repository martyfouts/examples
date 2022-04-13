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
#
# https://blender.stackexchange.com/questions/259443/cant-change-render-engine-inside-an-enum-using-blender-python
# Change render engines with an enum
from bpy.types import (Panel, Scene)

def updater(self, context):
    context.scene.render.engine = context.scene.my_enum0 
    
class TestPanel(bpy.types.Panel):
    bl_label = "Quick Render Presets"
    bl_idname = "PT_TestPanel"  
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Example'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "my_enum0")
    
classes = [TestPanel]
 
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    Scene.my_enum0 = bpy.props.EnumProperty(
            name= "",
            description= "Change the render engine of the scene",
            items= [('CYCLES', "Cycles", "f"),
                    ('BLENDER_EEVEE', "Eevee", "fg"),
            ],
            update=updater
        ) 

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_enum0