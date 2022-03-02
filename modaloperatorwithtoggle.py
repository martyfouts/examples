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
from bpy.types import Operator, Panel

# A modal operator that can be toggled on and off by a boolean property
# This is adapted from https://blender.stackexchange.com/a/117791/42221
# and was used in answer to https://blender.stackexchange.com/q/250733/42221

class TEST_OT_modal_operator(Operator):
    bl_idname = "test.modal"
    bl_label = "Demo modal operator"

    def modal(self, context, event):
        # Check to see if the toggle wants us to stop
        if not context.window_manager.test_toggle:
            context.window_manager.event_timer_remove(self._timer)
            print("done")
            return {'FINISHED'}
        print("pass through")
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # The timer allows the modal to periodically sample the state of the boolean
        self._timer = context.window_manager.event_timer_add(0.01, window=context.window)
        context.window_manager.modal_handler_add(self)
        print("modal")
        return {'RUNNING_MODAL'}

class TEST_PT_side_panel(Panel):
    """This is the parent of the whole mess"""
    bl_label = "TEST panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TEST"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        label = "Operator ON" if context.window_manager.test_toggle else "Operator OFF"
        self.layout.prop(context.window_manager, 'test_toggle', text=label, toggle=True)  

def update_function(self, context):
    print("invoke modal")
    # Start the modal if it's not running
    if self.test_toggle:
        bpy.ops.test.modal('INVOKE_DEFAULT')
    return

classes = [
    TEST_PT_side_panel,
    TEST_OT_modal_operator,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.test_toggle = bpy.props.BoolProperty(
         default = False,
         update = update_function
    )

def unregister():
    del bpy.types.WindowManager.test_toggle
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == '__main__':
    register()

