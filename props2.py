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
# This part demonstrates Collection and Enum properties
# and provides examples of properties groups, callbacks
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
from bpy.types import PropertyGroup
from bpy.props import CollectionProperty
from bpy.props import EnumProperty
from bpy.props import StringProperty

from collections import namedtuple

#-----------------------------------------------------------------------------
#
# The named tuple is only used to make it easy to document the
# elements of the item tuple used to describe each enum
# item.  The icon and number fields are optional
# so that items can default to ("ID", "name", "")
ItemTuple = namedtuple("ItemTuple", [
    "identifier",   # The identifier is used for Python access.
    "name",         # Name for the interface.
    "description",  # Used for documentation and tooltips.
    "icon",         # An icon string identifier or integer icon value
                    # (e.g. returned by :class:`bpy.types.UILayout.icon`)
    "Number",       # Unique value used as the identifier for this item 
                    # (stored in file data)
                    # Use when the identifier may need to change.
                    # If the *ENUM_FLAG* option is used,
    ],
    defaults=("", "NONE", 0)
)

# This is how you would use the named tuple for a full tuple
Items = [tuple(ItemTuple("RED", "red", "a red", "EVENT_R", 1)),
        tuple(ItemTuple("GREEN", "green", "a green", "EVENT_G", 2)),
        tuple(ItemTuple("BLUE", "blue", "a blue", "EVENT_B", 3))
]

#-----------------------------------------------------------------------------
#
# The Enum property can have a callback that generates the items list rather
# than relying on the list being passed as an argument.
# The callback must have two arguments: scene and context and must
# return the generated items list.
def items_callback(scene, context):
    # The same enum with a dynamic callback
    # Instead of items as tuples we give the name of the callback function
    #
    items = [
        ("RED", "red", "reddish"),
        ("GREEN", "green", "greenish"),
        ("BLUE", "blue", "not red-greenish")
    ]

    object = context.active_object
    if object and object.type == 'LIGHT':
        items.append(("MAG", "magenta", "?"))

    return items

#-----------------------------------------------------------------------------
#
# The CollectionProperty collects members of a class that has been
# derived from byp.types.PropertyGroup.
# https://docs.blender.org/api/current/bpy.types.PropertyGroup.html#bpy.types.PropertyGroup
# since this class must contain one or more properties, it must be registered.
class TOOL_property_group(PropertyGroup):
    """ Property Group used to demonstrate the CollectionProperty
    """
    name : bpy.props.StringProperty(name="name", default="Unknown")
    nickname : bpy.props.StringProperty(name="nickname", default="")

#-----------------------------------------------------------------------------
#
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
class TOOL_PT_collections(TOOL_Panel_common, Panel):
    """ Subpanel to demonstrate Collection properties """
    bl_label = "Collection Properties"
    bl_parent_id = TOOL_PT_Panel.bl_idname
    
    def draw(self, context):
        aCollection = context.scene.collection_general
        row = self.layout.row()
        row.label(text="Collection properties")
        row = self.layout.row()
        row.prop(context.scene, "collection_general")
        row = self.layout.row()
        colA = row.column()
        colB = row.column()
        colA.label(text="name")
        colB.label(text="nickname")
        for anItem in aCollection:
            colA.label(text=f"{anItem.name}")
            colB.label(text=f"{anItem.nickname}")


#-----------------------------------------------------------------------------
#
class TOOL_PT_enums(TOOL_Panel_common, Panel):
    """ Subpanel to demonstrate Enum properties """
    bl_label = "Enum Properties"
    bl_parent_id = TOOL_PT_Panel.bl_idname
    
    def draw(self, context):
        row = self.layout.row()
        row.label(text="Enum properties")
        row = self.layout.row()
        row.prop(context.scene, "enum_general")
        row = self.layout.row()
        row.prop(context.scene, "enum_simple")

#-----------------------------------------------------------------------------
#
classes = [
    TOOL_property_group,
    TOOL_PT_Panel,
    TOOL_PT_collections,
    TOOL_PT_enums,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.CollectionProperty
    Scene.collection_general = CollectionProperty(
        type=TOOL_property_group,
        name="names",
        description = "",
        options={'ANIMATABLE'},
        override = set(),
    )
    aCollection = bpy.context.scene.collection_general
    # This is only needed because during debugging the collection isn't deleted
    # Collections support four functions
    aCollection.clear() # remove all of the entries in the collection

    anItem = aCollection.add() # add a new default entry
    anItem.name = "Fouts"
    anItem.nickname = "Marty"

    anItem = aCollection.add()
    anItem.name = "Fouts"
    anItem.nickname = "Jeanne"
    
    # See https://blender.stackexchange.com/a/23637/42221 for move background
    # but it's move(source_index, target_index)
    # so one assumes that remove is remove(index)

    # https://docs.blender.org/api/current/bpy.props.html#bpy.props.EnumProperty
    Scene.enum_general = EnumProperty(
        items=Items, #  sequence of enum items (see above)
        name="color", # Name for the interface.  Must not be None
        description="", # Used for documentation and tooltips.
        default=None, #  The default value for this enum, a string from the
                # identifiers used in *items*, or integer matching an item number.
                # If the *ENUM_FLAG* option is used this must be a set of such
                # string identifiers instead.
                # WARNING: Strings can not be specified for dynamic enums
        options={'ANIMATABLE'},
        override=set(),
        update=None, 
        get=None,
        set=None
    )

    # An enum can be 'dynamic' if it has a callback that defines the items
    # rather than a list of items.  You can' set a default in this case.
    Scene.enum_simple = EnumProperty(
        items=items_callback,
        name="color",
    )

def unregister():
    del Scene.collection_general
    del Scene.enum_simple
    del Scene.enum_general
    for c in classes:
        bpy.utils.unregister_class(c)
        
if __name__ == '__main__':
    register()
