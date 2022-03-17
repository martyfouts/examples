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
import bmesh
import csv
# https://docs.python.org/3/library/csv.html

# Using CSV library to export and import vertices
csvFilename = r'C:\tmp\monkey.csv'

object = bpy.context.active_object
assert(object.type == "MESH")
# alternatively one could switch to edit mode via
# bpy.ops.object.mode_set(mode='EDIT')
if not object.mode == 'EDIT':
    bm = bmesh.new()
    bm.from_mesh(object.data)
else:
    bm = bmesh.from_edit_mesh(object.data)

verts = bm.verts
verts.ensure_lookup_table()

with open(csvFilename, 'w', newline='') as csvFile:
    csvwriter = csv.writer(csvFile, delimiter=',')
    for vert in verts:
        csvwriter.writerow([vert.index, vert.co.x, vert.co.y, vert.co.z])
        
with open(csvFilename, 'r') as csvFile:
    csvreader = csv.reader(csvFile, delimiter=',', 
        quotechar='|',
        quoting=csv.QUOTE_NONNUMERIC)
    for row in csvreader:
        print(f"{int(row[0])} is ({row[1]}, {row[2]}, {row[3]})")
        index = int(row[0])
        verts[index].co.z = row[3]

if not object.mode == 'EDIT':
    bm.to_mesh(object.data)
    bm.free()
else:
    bmesh.update_edit_mesh(object.data)

