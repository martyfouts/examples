import bpy
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
#------------------------------------------------------------------------------
#
# https://blender.stackexchange.com/questions/262213/how-to-delete-point-from-spline
# Create a curve with no control points

curve = bpy.data.curves.new(name='curve_data',type='CURVE')
curve.dimensions = '3D' 

curveObj = theObj = bpy.data.objects.new("curve_obj", curve)
bpy.context.collection.objects.link(curveObj)
polyline = curve.splines.new('POLY')

point = polyline.points[0]
point.select = True

bpy.context.view_layer.objects.active = curveObj
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.curve.delete(type='VERT')
