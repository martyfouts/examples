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

#-----------------------------------------------------------------------------
#
import bpy
from bpy.types import Operator, Panel
from enum import Enum


class Choice(Enum):
    Uninitialized = -1
    One = 0
    Two = 1
    Three = 3

class ButtonMachine:
    def __init__(self, initialState = Choice.Uninitialized):
        self.state = initialState

def nextState(state):
    currentState = states.get(state)
    if currentState:
        return currentState.nextState
    else:
        return None

class Transition:
    def __init__(self, newText = "None", newOperator = "None", newState = Choice.Uninitialized):
        self.displayText = newText
        self.stateOperator = newOperator
        self.nextState = newState

class MISC_OT_ButtonOneOperator(Operator):
    bl_idname = "scene.buttonone_operator"
    bl_label = "Add-On Function 1"
    
    def execute(self, context):
        machine.state = nextState(machine.state)
        return {'FINISHED'}

class MISC_OT_ButtonTwoOperator(Operator):
    bl_idname = "scene.buttontwo_operator"
    bl_label = "Add-On Function 2"
    
    def execute(self, context):
        machine.state = nextState(machine.state)
        return {'FINISHED'}

class MISC_OT_ButtonThreeOperator(Operator):
    bl_idname = "scene.buttonthree_operator"
    bl_label = "Add-On Function 2"
    
    def execute(self, context):
        machine.state = nextState(machine.state)
        return {'FINISHED'}

machine = ButtonMachine(Choice.One)

states = {
    Choice.One : Transition("- 1 -", "scene.buttonone_operator", Choice.Two),
    Choice.Two : Transition("- 2 -", "scene.buttontwo_operator", Choice.Three),
    Choice.Three : Transition("- 3 -", "scene.buttonthree_operator", Choice.One),
}

class MISC_PT_TestPanel(Panel):
    bl_label = "Test Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
            
    def draw(self, context):
        currentState = states.get(machine.state)
        if currentState:
            self.layout.label(text=currentState.displayText)
            self.layout.separator_spacer
            self.layout.operator(currentState.stateOperator)
            nextState = currentState.nextState
        else:
            self.layout.label(text="lost")
        
def register():
    bpy.utils.register_class(MISC_OT_ButtonOneOperator)       
    bpy.utils.register_class(MISC_OT_ButtonTwoOperator)       
    bpy.utils.register_class(MISC_OT_ButtonThreeOperator)       
    bpy.utils.register_class(MISC_PT_TestPanel)

def unregister():
    bpy.utils.unregister_class(MISC_OT_ButtonOneOperator)       
    bpy.utils.unregister_class(MISC_OT_ButtonTwoOperator)       
    bpy.utils.unregister_class(MISC_OT_ButtonThreeOperator)       
    bpy.utils.unregister_class(MISC_PT_TestPanel)
    
if __name__ == "__main__":
    register()