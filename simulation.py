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
# Setting up a smoke domain (like quick smoke)
def smoke_setup():
    object = bpy.context.object
    if not object:
        # There is no active object
        # you may want error handling or messaging here
        return

    if object.modifiers.get('Fluid'):
        # The active object already has a Fluid modifier
        # You may want error handling or messaging here
        return

    object.quick_smoke()
    object.modifiers["Fluid"].domain_settings.cache_type = 'ALL'
    # object.modifiers["Fluid"].domain_settings.cache_directory = '/tmp/blender_leBmMS/cache_foo'
    bpy.ops.fluid.bake_all()


smoke_setup()