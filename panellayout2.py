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

# Panel functionality demonstration part 2
# This part is an annotated demonstration of
# various UILayout methods other than those that are container-like
# This does not deal at all with the translation related
# method arguments.
# This part provides simple examples of prop, operator,
# menu and popover

bl_info = {
    "name" : "Annotated UI Layout Example",
    "description" : "Example of UI Layout functionality",
    "author" : "Marty Fouts <fouts@fogey.com>",
    "version" : (0, 0, 1),
    "blender" : (2, 93, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

import bpy
from bpy.types import Panel, Operator, Menu
from bpy.props import IntProperty # so we can have a property to demonstrate

#-----------------------------------------------------------------------------
#
# An extremely simple operator to demonstrate the operator method
class TOOL_OT_Operator(Operator):
    """ A very stupid operator entirely for the purpose of demonstration"""
    bl_idname = "tool.hello"
    bl_label = "push me"
    bl_description = "demonstration button"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "Button Pushed")
        return {'FINISHED'}

#-----------------------------------------------------------------------------
#
# An extremely simple menu using the extremely simple operator to
# demonstrate the menu method.
class TOOL_MT_Menu(Menu):
    """ A very simple menu entirely for the purpose of demonstration"""
    bl_idname = "TOOL_MT_Menu"
    bl_label = "Menu One"
    
    def draw(self, context):
        self.layout.operator("tool.hello")
        self.layout.operator("tool.hello", text="No! push me")

#-----------------------------------------------------------------------------
#
class TOOL_Panel_Common:
    bl_space_type = 'VIEW_3D' # defaults to 'EMPTY'
    bl_region_type = 'UI' # defaults to 'WINDOW'
    bl_category = "Tool"

#-----------------------------------------------------------------------------
#
# Not the demonstration class.  A popover panel used in the popup method
class TOOL_PT_Popover(TOOL_Panel_Common, Panel):
    """ A very simple popover panel entirely for the purpose of demonstration
    """
    bl_idname = "TOOL_PT_Popover"
    bl_label = "Popover One"
    bl_options = { "INSTANCED" }
    
    def draw(self, context):
        self.layout.label(text="pop pop")
        self.layout.menu(TOOL_MT_Menu.bl_idname, icon = "TRIA_RIGHT")

#-----------------------------------------------------------------------------
#
class TOOL_PT_Panel(TOOL_Panel_Common, Panel):
    """ Tool panel to demonstrate UILayout
    """
    bl_idname = "TOOL_PT_Panel"
    bl_label = "Panel One"
    bl_description = "Demonstration of UILayout Features"
    bl_options = {
        'HEADER_LAYOUT_EXPAND',
    }

    def draw(self, context):
        row = self.layout.row()
        row.alignment = "CENTER"
        row.label(text="Demonstrator", icon="BLENDER")

        row = self.layout.row()
        row.alignment = "CENTER"

        # There seems to be a problem with prop not drawing its icon.
        row.label(text="", icon="QUESTION")

        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.prop
        # There are many properties and each deserves its own category.  Here
        # we use a simple IntProperty so as to concentrate on the prop method.
        # The two positional arguments identify the Blender thing that the
        # property is attached to and the name of the property.  The text name
        # here should match the property name  in the register function. The
        # first argument should be of the same type as the property was
        # attached to in the register function.
        # ToDo: event and full_event but see
        # https://blender.stackexchange.com/a/79330/42221
        # ToDo: index
        row.prop(context.active_object, "int_thing",
            text=context.active_object.name,
            icon="QUESTION",
            expand=True, # Expand button to show more detail
            slider=True, # Use slider widget for numeric values
            toggle=True, # Use toggle widget for boolean values, or a checkbox
                        # when disabled
                        # (the default is -1 which uses toggle only when an icon
                        #  is displayed)
            icon_only = False, # Draw only icons in buttons, no text
            emboss=True, # Draw the button itself, not just the icon/text
            # icon_value=1, (See operator for details)
            invert_checkbox=False, # Draw checkbox value inverted
        )

        row = self.layout.row()
        row.alignment = "CENTER"

        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.operator
        # The first argument is a text string that matches the bl_idname of
        # the operator.  Since we have the operator class in the file, may as
        # well use the field.
        # Text overrides the operator's bl_label
        # icon_value is used in situations where the index of the icon in
        # the icon array is known, perhaps as an argument to the parent method
        # but the "Blender enum" text string is not.  See the source of the
        # icon viewer add-on for the relationship. 
        row.operator(TOOL_OT_Operator.bl_idname, 
            text="Button",
            #icon="INFO",
            icon_value=110, # The index of the INFO icon
            emboss=False, # Draw the button itself, not just the icon/text
            depress=True, # Draw pressed in (only works if emboss is True)
        )

        row = self.layout.row()
        row.alignment = "LEFT"
        
        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.menu
        # The simplest method. Can take icon_value instead of icon.
        row.menu(TOOL_MT_Menu.bl_idname, icon = "TRIA_RIGHT")

        row = self.layout.row()
        row.alignment = "LEFT"
        
        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.popover
        # The second simplest method. Can take either icon or icon_value.
        # The first argument must be a panel(?)
        row.popover(TOOL_PT_Popover.bl_idname)

#-----------------------------------------------------------------------------
#
classes = [
    TOOL_OT_Operator,
    TOOL_PT_Panel,
    TOOL_MT_Menu,
    TOOL_PT_Popover,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # A property just to demonstrate the prop method
    bpy.types.Object.int_thing = IntProperty(
        name = "just an integer",
        default = 17,
        min=0,
        max=10,
    )

def unregister():
    del bpy.types.Scene.int_thing
    for c in classes:
        bpy.utils.unregister_class(c)
        
if __name__ == '__main__':
    register()