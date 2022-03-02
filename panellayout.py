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

# Panel functionality demonstration part 1
# This part is an annotated demonstration of
# various panel aspects, concentrating mostly
# on the UILayout container-like methods

bl_info = {
    "name" : "Annotated Panel Example",
    "description" : "Example of panel functionality",
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
from bpy.types import Panel

# https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_space_type
# This may change between releases
# Note that 'EMPTY' isn't meant for use in Python .
bl_space_types = [
    'EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR',
    'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR',
    'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER',
    'PROPERTIES', 'FILE_BROWSER', 'SPREADSHEET', 'PREFERENCES'
]

# https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_region_type
# This may change between releases
bl_region_types = [
    'WINDOW', 'HEADER', 'CHANNELS', 'TEMPORARY', 'UI', 'TOOLS', 'TOOL_PROPS',
    'PREVIEW', 'HUD', 'NAVIGATION_BAR', 'EXECUTE', 'FOOTER', 'TOOL_HEADER', 'XR'
]

# https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_context
# bl_context is sort of a 'mode' of an editor, like object/edit/etc modes in
# the 3D viewport.  It's hard to pin down a useable list of contexts
# If you set bl_context, then the panel only appears in that context.

# https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_options
# This may change between releases
bl_option_choices = [
    'DEFAULT_CLOSED', 'HIDE_HEADER', 'INSTANCED', 'HEADER_LAYOUT_EXPAND'
] # defaults to 'DEFAULT_CLOSED'

#-----------------------------------------------------------------------------
#
# Panels usually come in groups and it is common to use a mixin class for
# all of the data that is identical for each panel in the group.
#
class TOOL_Panel_Common:
    bl_space_type = 'VIEW_3D' # defaults to 'EMPTY'
    bl_region_type = 'UI' # defaults to 'WINDOW'

    # https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_category
    # This is effectively the name of Tab that the panel will be displayed in
    # Tool is an existing tab, so this panel will be appended to it.
    bl_category = "Tool"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
#-----------------------------------------------------------------------------
#
# There's a naming convention for Panel classes. 3 items separated by '_'
# TOOL_PT_Panel
# ^    ^  ^
# |    |  +----  The actual name of your choice
# |    +-------  "PT" (for "Panel Type")
# +------------  The category of the panel in all upper case.
# It's meant to be used for bl_idname, but it's just as well to also
# use it for the class name.
#
# Every panel inherits from bpy.types.Panel
# https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel
#
class TOOL_PT_Panel(TOOL_Panel_Common, Panel):
    """ Tool panel to demonstrate Panel Class layout
    """

    # https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_idname
    # Defaults to class name
    bl_idname = "TOOL_PT_Panel"

    # https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_label
    # label at top of panel header next to collapse triangle
    bl_label = "Panel One"

    # Effectively, the panel's tooltip
    bl_description = "Demonstration of Panel Class Features"
    
    # options, see above
    bl_options = {
        'HEADER_LAYOUT_EXPAND',
    } # default open, don't hide header, not instanced, allow header stretching

    # https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.draw
    # This is the one method that the class must override.
    # https://docs.blender.org/api/current/info_best_practice.html#user-interface-layout
    # has tips for the layout
    def draw(self, context):
        self.layout.label(text="Small Class")

#-----------------------------------------------------------------------------
#
class TOOL_PT_Subpanel(TOOL_Panel_Common, Panel): 
    """ Demonstrate how to add a subpanel and show some layout
        Also implement poll and draw_header methods.
    """
    bl_label = "Subpanel One"
    bl_description = "Demonstration of a subpanel"
    bl_parent_id = "TOOL_PT_Panel"

    # https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_parent_id
    
    
    # https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.poll
    @classmethod
    def poll(cls, context):
        """ Only draw this panel when in Object mode """
        return context.mode == 'OBJECT'
    
    # https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.draw_header
    # There are usage recommendations for layout variable names:
    # https://docs.blender.org/api/current/info_best_practice.html#user-interface-layout
    # use row, col, split and flow for layouts of that type.
    # use sub for a sub layout.
    def draw_header(self, context):
        col = self.layout.column()
        col.label(text="", icon="EVENT_H")
    
    def draw(self, context):
        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout
        # There are a lot of layout functions specific to various
        # bpy things.  This is just a quick demo
        self.layout.label(text="Child class", icon="EVENT_C")
        # Add a row of Icons, just because
        row = self.layout.row()
        row.label(text="", icon="EVENT_M")
        row.label(text="", icon="EVENT_A")
        row.label(text="", icon="EVENT_R")
        row.label(text="", icon="EVENT_T")
        row.label(text="", icon="EVENT_Y")
        row = self.layout.row()
        row.label(text="", icon="EVENT_F")
        row.label(text="", icon="EVENT_O")
        row.label(text="", icon="EVENT_U")
        row.label(text="", icon="EVENT_T")
        row.label(text="", icon="EVENT_S")
        
#-----------------------------------------------------------------------------
#
class TOOL_PT_Layout(TOOL_Panel_Common, Panel): 
    """ Demonstrate the container-like layout methods """
    bl_label = "layout"
    bl_description = "Demonstration of container-like layout methods"
    bl_parent_id = "TOOL_PT_Panel"
    
    def draw(self, context):
        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout

        # Start with the rarely used box
        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.box
        # A box is a visual separation, based on being colored differently.
        box = self.layout.box()
        # properties affect the contents of the container
        box.alert = False  # If true everything in the box is tinted red
        box.scale_x = 1.0  # affects the initial scaling of the box
        box.scale_y = 1.0  # but the box is still resizable

        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.row
        # A row is a container.  Items are added to it from left to right.
        row = box.row()
        row.alignment = "CENTER"
        row.label(text="I'm a box!", icon="COLLECTION_COLOR_01")

        # This row contains three columns.  Each column contains 2 items.
        # A grid flow can accomplish a similar thing as can a
        # column flow but they automatically organize the content
        row = box.row()

        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.column
        col = row.column()
        col.alignment = "RIGHT"
        col.label(text="", icon="BACK")
        col.label(text="", icon="PLAY_REVERSE")
        col = row.column()
        col.alignment = "CENTER"
        col.label(text="", icon="TRIA_UP")
        col.label(text="", icon="TRIA_DOWN")
        col = row.column()
        col.alignment = "LEFT"
        col.label(text="", icon="FORWARD")
        col.label(text="", icon="PLAY")
        
        box = self.layout.box() # A new box
        box.alignment = "CENTER" # Doesn't appear to work
        box.label(text="Box", icon="COLLECTION_COLOR_02")

        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.column_flow
        flow = box.column_flow(columns=3)
        # Since the number of labels is divisible by 6, this fits evenly, but
        # It doesn't have the ability to align each column differently.
        flow.label(text="", icon="BACK")
        flow.label(text="", icon="PLAY_REVERSE")
        flow.label(text="", icon="TRIA_UP")
        flow.label(text="", icon="TRIA_DOWN")
        flow.label(text="", icon="FORWARD")
        flow.label(text="", icon="PLAY")
        
        
        box = self.layout.box() # A third box
        box.label(text="Box", icon="COLLECTION_COLOR_03")

        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.grid_flow
        # This transposes the columns because row_major is True.
        flow = box.grid_flow(columns=2, row_major=False)
        flow.label(text="", icon="BACK")
        flow.label(text="", icon="PLAY_REVERSE")
        flow.label(text="", icon="TRIA_UP")
        flow.label(text="", icon="TRIA_DOWN")
        flow.label(text="", icon="FORWARD")
        flow.label(text="", icon="PLAY")

#-----------------------------------------------------------------------------
#
# To use a class you have to register it.  This is a common idiom
# for registration of panels.
classes = [
    TOOL_PT_Panel,
    TOOL_PT_Subpanel,
    TOOL_PT_Layout,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
        
if __name__ == '__main__':
    register()