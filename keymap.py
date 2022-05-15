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
# 1) All keyconfigurations are stored in the window manager
#    https://docs.blender.org/api/current/bpy.types.KeyConfigurations.html
#
# 2) the top level KeyConfigurations object has a collection of KeyConfig
#    collections as well as 4 pointers to specific KeyConfigs 
#    https://docs.blender.org/api/current/bpy.types.KeyConfig.html#bpy.types.KeyConfig
#
# 3) a KeyConfig contains a collection of KeyMap objects
#    https://docs.blender.org/api/current/bpy.types.KeyMap.html#bpy.types.KeyMap
#
# 4) a KeyMap contains a collection of KeyMapItem objects.  These are the
#    actual shortcuts
#    https://docs.blender.org/api/current/bpy.types.KeyMapItem.html#bpy.types.KeyMapItem
#
# ToDo:
# KeyConfigurations find_item_from_operator() and update()
# KeyMaps find() and find_modal()
# KeyMap active(), restore_to_default(), and restore_item_to_default()
# KeyMapItems new_modal(), new_from_item(), from_id(), find_from_operator(),
#             and match_event()
# KeyMapItem compare()
#            add various fields to print
#            understand how KeyMapItem is used by the event handler


#####
# print functions
#
def print_keyconfiguration(keyconfiguration):
    """ function that prints some data about the members of a KeyConfiguration
        structure.  It does not iterate through the collections.
    """
    print("Key Configurations", end='')
    if keyconfiguration.active:
        print(f", Active: {keyconfiguration.active.name}", end='')
    if keyconfiguration.default:
        print(f", Default: {keyconfiguration.default.name}", end='')
    if keyconfiguration.addon:
        print(f", Addon: {keyconfiguration.addon.name}", end='')
    if keyconfiguration.user:
        print(f", User: {keyconfiguration.user.name}", end='')
    print(".")


def print_keyconfig(keyconfig):
    """ function that prints the members of a KeyConfig
        structure, except for the collection of KeyMap entries.
    """
    print(keyconfig.name, end='')
    if keyconfig.preferences:
        print(f".  has preferences ({keyconfig.preferences.bl_idname})", end='')
    if keyconfig.is_user_defined:
        print(f",  user defined", end='')
    print('.')

def print_keymap_entry(keymap):
    """ function that prints the members of a KeyMap.
        It does not iterate through the collection of KeyMapItem objects.
    """
    print(f"{keymap.name}: ", end='')
    active_entry = keymap.active()
    if active_entry:
        print(f" active entry is {active_entry.name}", end='')
    if keymap.bl_owner_id:
        print(f" owner is {keymap.bl_owner_id}", end='')
    if keymap.is_modal:
        print(f", modal", end='')
    if keymap.is_user_modified:
        print(f", user modified", end='')
    print(f", {keymap.region_type}", end='')
    print(f", {keymap.space_type}", end='')
    print(".")

def print_modifiers(item):
    """ Helper function for KeyMapItem printer """
    if item.alt:
        print(" Alt", end='')
    if item.ctrl:
        print(" Ctrl", end='')
    if item.shift:
        print(" Shift", end='')
    if item.key_modifier and item.key_modifier != "NONE":
        print(f" {item.key_modifier}", end='')

def print_keymap_item(item):
    print(f"{item.name}:", end='')
    if not item.active:
        print(" inactive")
    else:
        print(" active", end='')
        print(f" {item.idname}: ", end='')
        print_modifiers(item)
        print(f" {item.to_string()} ({item.type})", end='')
        if item.is_user_defined:
            print(", user defined", end='')
        if item.is_user_modified:
            print(", modified", end='')
        print('.')

def print_keymap_items(keymap):
    """ Helper function to iterate through collection
        of KeyMapItem.
    """
    for item in keymap.keymap_items:
        print_keymap_item(item)


# In typical use there is only one KeyConfigurations object
# it is attached to the WindowManager object.
keyconfigs = bpy.context.window_manager.keyconfigs

# Use the default KeyMap collection.
default_keymaps = bpy.context.window_manager.keyconfigs.default.keymaps

# Pick a specific KeyMap to use as an example
keymap = default_keymaps['Window']

# Print some info about the keyconfigurations
print_keyconfiguration(keyconfigs)

# Print all of the keyconfig names
for keyconfig in keyconfigs:
    print_keyconfig(keyconfig)

print_keymap_entry(keymap)
print_keymap_items(keymap)


#-----------------------------------------------------------------------------
# print all of the keymap items that use the same Key

for keyconfig in bpy.context.window_manager.keyconfigs:
    for keymap in keyconfig.keymaps:
        for item in keymap.keymap_items:
            if item.type == 'P' and item.ctrl:
                print(f"{keyconfig.name}: {keymap.name}: {item.name} ", end='')
                print_keymap_item(item)
                
#-----------------------------------------------------------------------------
# create a new keyconfig, with a new keymap, and give it a new item

new_keyconfig = bpy.context.window_manager.keyconfigs.new("newkc")
new_keymap = new_keyconfig.keymaps.new(
    "newkm",
    space_type = "VIEW_3D",
    region_type = "WINDOW",
    modal = False,
    tool = False
)

new_keymap_item = new_keymap.keymap_items.new(
    "wm.call_menu",
    type = 'A',
    value = 'PRESS',
    any = False,
    ctrl = 0,
    alt = 0,
    oskey = 0,
    key_modifier = 'NONE',
    repeat = False,
    head = False
)

print(f"{keyconfig.name}: {keymap.name}: {item.name} ", end='')
print_keymap_item(new_keymap_item)

# undo the above
new_keymap.keymap_items.remove(new_keymap_item)
new_keyconfig.keymaps.remove(new_keymap)
bpy.context.window_manager.keyconfigs.remove(new_keyconfig)

#-----------------------------------------------------------------------------
# registering a shortcut for a custom operator.

from bpy.types import Operator

class TLA_OT_keyhit(Operator):
    """ speak about the keymap hit """
    bl_idname = "kmap.keyhit"
    bl_label = "Print something"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        self.report({'INFO'},
            f"keyhit execute()")
        return {'FINISHED'}

classes = [
    TLA_OT_keyhit,
]

def register():
    keymap = bpy.context.window_manager.keyconfigs.addon.keymaps.new(
        name='3D View',
        space_type='VIEW_3D'
    )
    keymap.keymap_items.new(
        'kmap.keyhit',
        type='W',
        value='PRESS',
        ctrl=True,
    )
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    keymap = bpy.context.window_manager.keyconfigs.addon.keymaps.new(
        name='3D View',
        space_type='VIEW_3D'
    )
    for item in keymap.keymap_items:
        if item.idname == 'kmap.keyhit':
            keymap.keymap_items.remove(item)
