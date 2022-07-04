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

# https://blender.stackexchange.com/questions/268368/how-to-change-the-target-object-of-a-copy-location-constraint-using-python
# Adding a constraint to selected objects
# This is an example of adding copy location constraints to objects
# It adds a constraint to every selected objects except the active
# setting the target to the active object.

src_obj = bpy.context.active_object

def get_constraint(obj, name, type):
    """ return the first constraint with name name for obj
        if there isn't one add one of type type and return it
    """
    try:
        con = obj.constraints[name]
    except KeyError:
        con = obj.constraints.new('COPY_LOCATION')
    return con

for dst_obj in bpy.context.selected_objects:
    if dst_obj is src_obj:
        continue
    print(dst_obj.name)
    con = get_constraint(dst_obj, 'Copy Location', 'COPY_LOCATION')
    con.target = src_obj
    con.target_space = 'LOCAL'
    con.owner_space = 'LOCAL'
