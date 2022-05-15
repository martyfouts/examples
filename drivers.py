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
# example from user Kolupsy on bpy Discord server python questions channel
# How to add a driver to an object
# https://docs.blender.org/api/current/bpy.types.bpy_struct.html#bpy.types.bpy_struct.driver_add
obj = bpy.context.object

driver = obj.driver_add( 'location', 0 ).driver #create the driver
driver.type = 'SCRIPTED' #be able to set the expression
var = driver.variables.new( ) #make a new variable
var.name = 'frame' #set the variables name
var.type = 'SINGLE_PROP' #use a python attribute instead of transforms
target = var.targets[0] #get the first target. depending on the variable type
                        # you could have a different amount of targets
target.id_type = 'SCENE' #set the id_type for the ID object you want as a target
target.id = bpy.context.scene #set the ID object itself
target.data_path = 'frame_current' #set the python attribute you want to use from
                        # the ID object
driver.expression = var.name #set the expression of the driver. keep in mind that 
                        # this is not an equation but the right hand side of a 
                        # FLOAT variable definition