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

# 
# This is an annotated demonstration of Property classes
#
# This part demonstrates Properties built from primitives
# or vectors of primitives.
# Collection and Enum properties are deferred to a later
# part, as are examples of properties groups, callbacks
# and the setter/getter pattern

# hhttps://docs.blender.org/api/current/bpy.props.html

bl_info = {
    "name" : "Annotated Property Example",
    "description" : "Example of Primitive/Vector Properties",
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
from bpy.types import Panel, Scene

# A complete list of property types, current in Blender 3.0
# The basic use of a property is to provide a way of extending the Blender
# internal type system by assigning properties that Blender can locate
# through its internal naming scheme.
#
# A property is created by calling a function of the same name.  The
# function sets up some C code that will be invoked at a later time
# to introduce the property into the name space.
#
# Properties extend classes and are visible to various parts of the UI.
# For instance, the operator redo panel presents the properties of the
# operator so that they can be adjusted.
#
# Properties extend existing types. Once a property is added to a type
# any instance of that type wil have the property.  When the documentation
# refers to 'data' it means an instance of type type a property has been
# associated with.
#
# the text "name" of the property in the prop function is the same as
# the member name used for the property when the property is
# created by a call like bpy.type.CLASS.name = PropTypeProperty(...)
from bpy.props import BoolProperty, BoolVectorProperty
from bpy.props import CollectionProperty
from bpy.props import EnumProperty
from bpy.props import FloatProperty, FloatVectorProperty
from bpy.props import IntProperty, IntVectorProperty
from bpy.props import PointerProperty
from bpy.props import StringProperty


class TOOL_Panel_common:
    """ mixin class with common properties shared by all the Tools panels
        in this script.
    """
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_options = {"DEFAULT_CLOSED"}

#-----------------------------------------------------------------------------
#
class TOOL_PT_Panel(TOOL_Panel_common, Panel):
    """ Tool panel to demonstrate properties in various forms
    """
    bl_idname = "TOOL_PT_Panel"
    bl_label = "Properties"
    bl_description = "Demonstration of Property Features"

    def draw(self, context):
        row = self.layout.row()
        row.label(text="Display of properties")


#-----------------------------------------------------------------------------
#
class TOOL_PT_booleans(TOOL_Panel_common, Panel):
    """ Subpanel to demonstrate Boolean properties """
    bl_label = "Boolean Properties"
    bl_parent_id = TOOL_PT_Panel.bl_idname
    
    def draw(self, context):
        row = self.layout.row()
        row.label(text="Boolean properties")
        # How to add a property to a panel layout. This one time only,
        # all of the options are given, along with their default values.
        # Only the first two, data and property are required.  All others
        # are keyword and have defaults.
        # As usual, translation arguments are ignored.
        # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.prop
        row = self.layout.row()
        row.prop(context.scene, # Data from which to take property
                    "bool_general", # Identifier of property in data
                    text="Simple Stuff", # Override automatic text of the item
                    icon="NONE", # an enum fro a vast selection
                    expand=False, # Expand button to show more detail
                    slider=False, # Use slider widget for numeric values
                    toggle=-1, # Use toggle widget for boolean values, or 
                                # a checkbox when disabled (the default 
                                # is -1 which uses toggle only when an icon
                                # is displayed)
                    icon_only=False, # Draw only icons in buttons, no text
                    event=False, # Use button to input key events
                    full_event=False, # Use button to input full events
                                        # including modifiers
                    emboss=True, #  Draw the button itself, not just the
                                    # icon/text. When false, corresponds to 
                                    # the ‘NONE_OR_STATUS’ layout emboss type
                    index=-1, # The index of this button, when set a single
                                # member of an array can be accessed, when set
                                # to -1 all array members are used
                    icon_value=-1, # Icon Value, Override automatic icon of 
                                    # the item
                    invert_checkbox=False # Draw checkbox value inverted
        )
        row = self.layout.row()
        row.prop(context.scene, "bool_vector", text="vector")


#-----------------------------------------------------------------------------
#
class TOOL_PT_floats(TOOL_Panel_common, Panel):
    """ Subpanel to demonstrate Float properties """
    bl_label = "Float Properties"
    bl_parent_id = TOOL_PT_Panel.bl_idname
    
    def draw(self, context):
        row = self.layout.row()
        row.label(text="Floating Point properties")
        row = self.layout.row()
        row.prop(context.scene, "float_general")
        row = self.layout.row()
        row.prop(context.scene, "float_factor")
        row = self.layout.row()
        row.prop(context.scene, "float_distance")
        row = self.layout.row()
        row.prop(context.scene, "float_vector_rgb")
        row = self.layout.row()
        row.prop(context.scene, "float_vector_rgba")
        row = self.layout.row()
        row.prop(context.scene, "float_vector_translation")
        row = self.layout.row()
        row.prop(context.scene, "float_vector_direction")
        row = self.layout.row()
        row.prop(context.scene, "float_vector_velocity")
        row = self.layout.row()
        row.prop(context.scene, "float_vector_acceleration")
       
#-----------------------------------------------------------------------------
#
class TOOL_PT_ints(TOOL_Panel_common, Panel):
    """ Subpanel to demonstrate Int properties """
    bl_label = "Int Properties"
    bl_parent_id = TOOL_PT_Panel.bl_idname
    
    def draw(self, context):
        row = self.layout.row()
        row.label(text="Integer properties")
        row = self.layout.row()
        row.prop(context.scene, "int_general")
        row = self.layout.row()
        row.prop(context.scene, "int_vector_general")

#-----------------------------------------------------------------------------
#
class TOOL_PT_strings(TOOL_Panel_common, Panel):
    """ Subpanel to demonstrate String properties """
    bl_label = "String Properties"
    bl_parent_id = TOOL_PT_Panel.bl_idname
    
    def draw(self, context):
        row = self.layout.row()
        row.label(text="String properties")
        row = self.layout.row()
        row.prop(context.scene, "string_general")
        row = self.layout.row()
        # displays with the file browser
        row.prop(context.scene, "string_file_path")
        row = self.layout.row()
        # displays with the file browser set to accept directories
        row.prop(context.scene, "string_dir_path")
        row = self.layout.row()
        row.prop(context.scene, "string_file_name")
        row = self.layout.row()
        # ignores character escapes
        row.prop(context.scene, "string_byte_string")
        row = self.layout.row()
        # displays '*'s doesn't report info
        row.prop(context.scene, "string_password")
                    
property_options = ["HIDDEN", "SKIP_SAVE", "ANIMATABLE", "LIBRARY_EDITABLE",
                    "PROPORTIONAL","TEXTEDIT_UPDATE"]
                    
# Subtypes are meaningless for bool types
# Subtypes that mean anything for float Property
# ['PIXEL', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'DISTANCE', 'POWER', 'TEMPERATURE']

# Units for float Property
# ['LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY',
#  'ACCELERATION', 'MASS', 'CAMERA', 'POWER']

#-----------------------------------------------------------------------------
#
classes = [
   TOOL_PT_Panel,
   TOOL_PT_booleans,
   TOOL_PT_floats,
   TOOL_PT_ints,
   TOOL_PT_strings,
]

# for the demonstration all properties are attached to the bpy.types.Scene type
# and are accessed through context.scene.
def register():
    for c in classes:
        bpy.utils.register_class(c)

    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.BoolProperty
    # This one time only, all of the options are given, along with their
    # default values. Only the name is requires. It is the text string that
    # appears in the UI Layout unless it is overridden by the 'text=' argument
    # of the prop function
    Scene.bool_general = BoolProperty(name="general boolean",
        description="A simple Boolean property", # Text used for the tooltip 
                                                 # and api documentation.
        default = False, # 
        options = {'ANIMATABLE'}, # see property_options above
        override = set(), # {'LIBRARY_OVERRIDABLE'}
        #tags = set(), #  Enumerator of tags that are defined by parent class.
        subtype = "NONE",
        update = None, #  Function to be called when this value is modified,
                        #  This function must take 2 values (self, context)
                        #  and return None.
        set = None, # Function to be called when this value is 'read',
                    # This function must take 1 value (self) and return the value of the property.
        get = None, # Function to be called when this value is 'written',
                    # This function must take 2 values (self, value) and return None.
    )
    
    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.BoolVectorProperty
    # Boolean Vectors have exactly the same arguments as Boolean with the
    # addition of the size argument and the default object taking a sequence
    Scene.bool_vector = BoolVectorProperty(name="vector boolean",
        default = [ False ] * 5, # sequence of booleans the length of size.
        size = 5, # Vector dimensions in [1, 32]. An int sequence can be
                    #  used to define multi-dimension arrays.
    )

    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.FloatProperty
    Scene.float_general = FloatProperty(name="general float", 
        subtype="NONE",
        default = 0.0, # Default value
        min = -3.0e+38, # Hard minimum, trying to assign a value below
                        # will silently assign this minimum instead.
        max = 3.0e+38, # Hard maximum
        soft_min = -3.0e+38, # Soft minimum (>= *min*), user won't be able to 
                            # drag the widget below this value in the UI
        soft_max = 3.0e+38, # Soft maximum (<= *max*)
        step = 3, # Step of increment/decrement in UI, in [1, 100],
                    # defaults to 3 (WARNING: actual value is /100).
        precision = 2, # Maximum number of decimal digits to display, 
                    # in [0, 6]
        options = {'ANIMATABLE'}, # see property_options above
        override = set(), # {'LIBRARY_OVERRIDABLE'}
        #tags = set(), #  Enumerator of tags that are defined by parent class.
        update = None, # see BoolProperty
        set = None, # see BoolProperty
        get = None, # see BoolProperty
        unit = "NONE"
    )

    # Float subtypes do some unit validation on input. You can use 'cm'
    # in the DISTANCE subtype for example. Rather than add a property
    # for each subtype, will use factor and distance for examples.
    Scene.float_factor = FloatProperty(name="factor", subtype="FACTOR",
        min=-10.0, max=10.0, soft_min=-5.0, soft_max=5.0, step=1, precision=1)
    Scene.float_distance = FloatProperty(name="distance", subtype="DISTANCE")
    
    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.FloatVectorProperty
    # The subtype is far more important in a FloatVector as it actually controls
    # the UI used to present the vector. As with BoolVector, there is an
    # added size argument and the default takes an array
    # The enums for subtype are different than for scalar float
    Scene.float_vector_general = FloatVectorProperty(name = "general vector float",
        default = [0.0] * 2, size = 2)
    # the size is critical for most float vectors
    # for "COLOR", 3 gets an RGB display, 4 gets a RGBA display, and anything
    # else goes back to the general format.
    Scene.float_vector_rgb = FloatVectorProperty(name = "color rgb",
        default = [0.5] * 3, size = 3, subtype = "COLOR")
    Scene.float_vector_rgba = FloatVectorProperty(name = "color rgba",
        default = [0.5] * 4, size = 4, subtype = "COLOR")
    # translation must be 3. each field with be distance unit.
    Scene.float_vector_translation = FloatVectorProperty(name = "translation",
        default = [0.5] * 3, size = 3, subtype = "TRANSLATION")
    # direction must be 3. displays the vector ball 
    Scene.float_vector_direction = FloatVectorProperty(name = "direction",
        default = [0.5] * 3, size = 3, subtype = "DIRECTION")
    # velocity must be 3. Display is m/s (responds to Scene units settings)
    Scene.float_vector_velocity = FloatVectorProperty(name = "velocity",
        default = [0.5] * 3, size = 3, subtype = "VELOCITY")
    # acceleration must be 3. Display is m/s^2 (responds to Scene units settings)
    Scene.float_vector_acceleration = FloatVectorProperty(name = "acceleration",
        default = [0.0, 0.0, 9.8], size = 3, subtype = "ACCELERATION")
    # ToDo: Matrix, Euler, Quaternion, Axis Angle, XYZ, XYZ Length,
    #       Color Gamma, Coordinates, Layer, and Layer Member

    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.IntProperty
    # Since subtype is demonstrated by the floating point properties
    # only one int property is demonstrated, but see int vectors.
    Scene.int_general = IntProperty(name="general", 
        subtype="NONE",
        default = 0, # Default value
        min = -2**31, # Hard minimum, trying to assign a value below
                        # will silently assign this minimum instead.
        max = 2**31-1, # Hard maximum
        soft_min = -2*31, # Soft minimum (>= *min*), user won't be able to 
                            # drag the widget below this value in the UI
        soft_max = 2**31-1, # Soft maximum (<= *max*)
        step = 1, # Step of increment/decrement in UI, in [1, 100],
                    # defaults to 3 (WARNING: actual value is /100).
        options = {'ANIMATABLE'}, # see property_options above
        override = set(), # {'LIBRARY_OVERRIDABLE'}
        #tags = set(), #  Enumerator of tags that are defined by parent class.
        update = None, # see BoolProperty
        set = None, # see BoolProperty
        get = None, # see BoolProperty
    )
    Scene.int_vector_general = IntVectorProperty(name="general vector int",
        default = [17] * 5, size = 5)

    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.StringProperty
    Scene.string_general = StringProperty(name="A String", default="Read Me")
    Scene.string_file_path = StringProperty(name="File Path", subtype="FILE_PATH")
    Scene.string_dir_path = StringProperty(name="Dir Path", subtype="DIR_PATH")
    Scene.string_file_name = StringProperty(name="File Name", subtype="FILE_NAME")
    Scene.string_byte_string = StringProperty(name="Byte String", subtype="BYTE_STRING")
    Scene.string_password = StringProperty(name="Password", subtype="PASSWORD")


def unregister():
    del Scene.string_password
    del Scene.string_byte_string
    del Scene.string_file_name
    del Scene.string_dir_path
    del Scene.string_file_path
    del Scene.string_general
    del Scene.int_vector_general
    del Scene.int_general
    del Scene.float_vector_acceleration
    del Scene.float_vector_velocity
    del Scene.float_vector_direction
    del Scene.float_vector_translation
    del Scene.float_vector_rgba
    del Scene.float_vector_rgb
    del Scene.float_vector_general
    del Scene.float_distance
    del Scene.float_factor
    del Scene.float_general
    del Scene.bool_vector
    del Scene.bool_general
    for c in classes:
        bpy.utils.unregister_class(c)
        
if __name__ == '__main__':
    register()