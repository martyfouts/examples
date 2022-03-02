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

#-----------------------------------------------------------------------------
#
# accessing cycles preferences
deviceList = bpy.context.preferences.addons["cycles"].preferences.get_devices()
for deviceTuple in deviceList:
    print("Devices:")
    for device in deviceTuple:
        print(f"\t{device.name} ({device.type}) {device.use}")

#-----------------------------------------------------------------------------
#
# How to fill an enum from a list
object_list = [('None', 'None', '')]
camera_list = [('None', 'None', '')]
light_list = [('None', 'None', '')]

for obj in bpy.context.scene.objects:    
    if obj.type == "CAMERA":
        camera_list.append((obj.name, obj.name, 'camera'))
    if obj.type == "LIGHT":
        light_list.append((obj.name, obj.name, 'light'))
    if obj.type == "MESH":
        object_list.append((obj.name, obj.name, 'mesh'))

class Enums(bpy.types.PropertyGroup):
    camera_enum : bpy.props.EnumProperty(
        name= "", 
        description= "None", 
        items= [("None", "None", ""),  # <-- Option to select none of the items
        ]
            
    )
    lights_enum : bpy.props.EnumProperty(
        name= "", 
        description= "None", 
        items= [("None", "None", ""),  # <-- Option to select none of the items
        ]
            
    )
    objects_enum : bpy.props.EnumProperty(
        name= "", 
        description= "None", 
        items= object_list,
    )

#-----------------------------------------------------------------------------
#
import random
from math import trunc

def unweighted_choice(intervals):
    """ Given a list of N tuples containing (start, end) intervals
        return a random number from one of the intervals.
        Each interval has a 1 in N chance of being used
    """
    n = trunc(random.uniform(0,len(intervals)))
    s = intervals[n]
    return random.uniform(s[0], s[1])


def prepare_cumulative_weights(intervals):
    """ Given a list of N tuples containing (start, end) intervals
        returns a list that uses the interval length of each tuple
        to assign it a cumulative position in a range that extends from 0 to
        the sum of all of the interval lengths.  This effectively assigns a
        weight to the tuple equivalent to the length of its interval.
    """
    weights = []
    t = 0.0
    for (s, e) in intervals:
        r = abs(s - e)
        t += r
        weights.append(t)
    return weights

def assign_cumulative_weights(raw_weights):
    """ Given a list of raw weights return a list of cumulative raw weights
    """
    weights = []
    t = 0.0
    for r in raw_weights:
        t += r
        weights.append(t)
    return weights

def weighted_choice(intervals, cumulative_weights):
    """ Given a list of N tuples containing (start, end) intervals
        and a list of cumulative weights, assigned from a monotic sequence
        returns a random number.  Each tuple has a chance of
        being selected from that is proportional to its weight.
    """
    f = random.uniform(0, cumulative_weights[-1])
    for n in range(0, len(cumulative_weights)):
        if cumulative_weights[n] > f:
            interval = intervals[n]
            return random.uniform(interval[0], interval[1])
    return -1

if __name__ == '__main__':
    intervals = [(1, 3), (4, 5), (7, 11)]
    raw = [7, 1, 1]
    u = unweighted_choice(intervals)
    print(f'An unweighted choice {u}')
    cumulative_intervals = prepare_cumulative_weights(intervals)
    for i in range(1,3):
        w = weighted_choice(intervals, cumulative_intervals)
        print(f'Length Weighted choice {i} {w}')
    cumulative_raw = assign_cumulative_weights(raw)
    for i in range(1,3):
        w = weighted_choice(intervals, cumulative_raw)
        print(f'Raw Weighted choice {i} {w}')

#-----------------------------------------------------------------------------
#
# How to make a collection the active collection
# see https://devtalk.blender.org/t/set-active-collection/2409
#
# This works for the latest collection because collections are added to
# the end of the view layer list:
collection = bpy.data.collections.new("MyTestCollection") # Create the collection
bpy.context.scene.collection.children.link(collection)  # Link it to the scene
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]

#-----------------------------------------------------------------------------
#
# how to call an exporter with a filter
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper
class TEST_OT_export_tst(Operator, ExportHelper):
    bl_idname = 'test.export_tst'
    bl_label = 'test export test'
    bl_options = {'PRESET', 'UNDO'}
 
    filename_ext = '.dat'
    
    filter_glob: StringProperty(
        default='*.dat',
        options={'HIDDEN'}
    )
 
    def execute(self, context):
        print('exported file: ', self.filepath)
        # Replace the 'obj' in the next line with the appropriate exporter
        # if you're using an exporter that already exists, or put your
        # code to write output in its place.
        bpy.ops.export_scene.obj(filepath=self.filepath)
        return {'FINISHED'}


#-----------------------------------------------------------------------------
#
# Example of a context override
# from https://blender.stackexchange.com/questions/254903/align-active-camera-to-view
# the only override you actually need is the area override
win = bpy.context.window
scr = win.screen
areas3d  = [area for area in scr.areas if area.type == 'VIEW_3D']
region   = [region for region in areas3d[0].regions if region.type == 'WINDOW']

override = {
    'window': win,
    'screen': scr,
    'area'  : areas3d[0],
    'region': region[0],
    'scene' : bpy.context.scene,
}

bpy.ops.view3d.camera_to_view(override)

# Simplifies to
areas3d  = [area for area in bpy.context.window.screen.areas if area.type == 'VIEW_3D']
bpy.ops.view3d.camera_to_view({'area':areas3d[0]})

#-----------------------------------------------------------------------------
#
# Example of using Custom Icons (like the brush icons)
# https://blender.stackexchange.com/questions/252366/use-new-icons-in-custom-interface/252380
#
# See https://devtalk.blender.org/t/how-to-get-toolbar-icons-names/6541
#
from bl_ui.space_toolsystem_common import ToolSelectPanelHelper

class PreviewsExamplePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Previews Example Panel"
    bl_idname = "OBJECT_PT_previews"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    def draw(self, context):
        layout = self.layout
        #pcoll = icons_dict["draw"]
        row = layout.row()
        #my_icon = pcoll["draw"]
        #row.operator("render.render", text="", icon_value=my_icon.icon_id)
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle('brush.sculpt.draw')
        row.operator("render.render", text="", icon_value=icon_id)

def register():
    bpy.utils.register_class(PreviewsExamplePanel)
    
def unregister():
    bpy.utils.unregister_class(PreviewsExamplePanel)

icons = []

cls = ToolSelectPanelHelper._tool_class_from_space_type('VIEW_3D')
for item_group in cls.tools_from_context(bpy.context):
    if type(item_group) is tuple:
        index_current = cls._tool_group_active.get(item_group[0].idname, 0)
        for sub_item in item_group:
            print(sub_item.label)
            icons.append(sub_item.icon)
    else:
        if item_group is not None:
            print(item_group.label)
            icons.append(item_group.icon)

#-----------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/252020/how-to-display-a-fixed-list-of-rgb-values-in-a-panel-and-when-a-color-is-clicked
# Example of creating and using image previews as icons.
#
# This function is derived from code taken
# from https://blender.stackexchange.com/a/652/42221
def new_icon(name, red, green, blue, alpha):
    icon_size = 32
    icon_image = bpy.data.images.new(name, width = icon_size, height = icon_size)
    pixels = [ None ] * icon_size * icon_size
    for x in range(icon_size):
        for y in range(icon_size):
            pixels[(y * icon_size) + x] = [red, green, blue, alpha]
    # Flatten List
    pixels = [chan for px in pixels for chan in px]
    icon_image.pixels = pixels
    return icon_image

palette = {
    "Red": (1.0, 0.0, 0.0, 1.0), 
    "Green": (0.0, 1.0, 0.0, 1.0), 
    "Blue": (0.0, 0.0, 1.0, 1.0), 
}

def make_icons(palette):
    icon_list = []
    for entry in palette:
        rgba = palette[entry]
        new_image = new_icon(entry, rgba[0], rgba[1], rgba[2], rgba[3])
        icon_list.append(new_image)
    return icon_list

icons = make_icons(palette)

class TLA_OT_Icon(bpy.types.Operator):
    """A button per color"""
    bl_idname = "tla.icon"
    bl_label = "Color"
    bl_description = "Pick color"
    bl_options = {'REGISTER', 'UNDO'}
    color: bpy.props.StringProperty(name="color")
    def execute(self, context):
        rgba= palette[self.color]
        self.report({'INFO'}, f"{self.color} {rgba} chosen")
        return {'FINISHED'}

# From https://blender.stackexchange.com/a/48508/42221
class TLA_PT_Icons(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Palette"
    bl_label = "Palette"
    def draw(self, context):
        layout = self.layout
        for image in icons:
            layout.operator("tla.icon", text="", icon_value=image.preview.icon_id).color=image.name
        if not icons:
            layout.label(text="No Colors in Palette")

classes = [
    TLA_OT_Icon,
    TLA_PT_Icons,
]

def register():
    for aclass in classes:
        bpy.utils.register_class(aclass)


def unregister():
    for aclass in classes:
        bpy.utils.unregister_class(aclass)
