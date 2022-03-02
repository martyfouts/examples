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
import pathlib
import sys

#------------------------------------------------------------------------------
# how to find the path to the current blend file
blender_file_path = pathlib.Path(bpy.data.filepath)
if bpy.data.filepath == '':
    print('You are working from an unsaved Blend file.  Do you really want to do that?')
else:
    print(f'You are working from file "{blender_file_path.name}"'
        + f' in directory (folder) {blender_file_path.parent}')

#------------------------------------------------------------------------------
# How to add the current path to the search path for imports
# Note that Blender does not support PYTHONPATH without the
# --python-use-system-env flag.  (See https://developer.blender.org/D6598)

if (blender_file_path.parent.exists()
    and not blender_file_path.parent in sys.path):
    sys.path.append(blender_file_path.parent)
    print(f'Adding path to sys.path')

#------------------------------------------------------------------------------
# How to make sure that a script is reimported
import importlib
try:
    import paths
except ModuleNotFoundError:
    print('snippets.py not on path')
else:
    importlib.reload(paths)
    print('snippets.py reloaded')
    
#------------------------------------------------------------------------------
# Say somethings about this instance of Blender
print(f'path to blender executable is {bpy.app.binary_path}')
print(f'path to blender python executable is {sys.executable}')

if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        print(f'\targ: {sys.argv[i]}')

print(f'version {bpy.app.version_string} date {bpy.app.build_commit_date}')

#------------------------------------------------------------------------------
# I should like to derive this from my home directory but because I've
# mapped Documents to another drive, I can't.
# blender_TLD = pathlib.home() / 'Documents' / 'blender'
blender_TLD =  pathlib.Path('D:/stupi/blender')
blender_python_directory = blender_TLD / 'python'

if blender_python_directory.exists():
    print(f'Adding {blender_python_directory} to python search path')
    if not blender_python_directory in sys.path:
        sys.path.append(str(blender_python_directory))

# How to execute a script in the python directory
script_file_name = 'introBPY.py'
script_file_path = blender_python_directory / script_file_name

if script_file_path.exists():
    exec(compile(open(script_file_path).read(), script_file_path, 'exec'))
else:
    print(f'Script {script_file_name} does not exist in path {blender_python_directory}')

#------------------------------------------------------------------------------
# How to set up the default directories for standard builds in the
# three most common operating systems.
# See https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html
# for an explanation of where these strings come from and how they're used
#
version = bpy.data.version
version_string = str(version[0]) + '.' + str(version[1])
# See https://docs.python.org/3.9/library/sys.html#sys.platform
# for the supported list.  In this example I only picked a
# couple to show the outline
#
LOCAL = pathlib.Path('./' + version_string)

if pathlib.sys.platform == 'win32':
    WIN32_USER = pathlib.Path(pathlib.os.getenv('USERPROFILE'))
    USER = WIN32_USER / 'AppData/Roaming/Blender Foundation' / version_string
    SYSTEM = USER
elif pathlib.sys.platform == 'linux':
    LINUX_USER = pathlib.Path(pathlib.os.getenv('HOME'))
    USER = LINUX_USER / '.config/blender' / version_string
    SYSTEM = pathlib.Path('/usr/share/blender/' + version_string)
elif pathlib.sys.platform == 'darwin':
    MACOS_USER = pathlib.Path(pathlib.os.getenv('USER'))
    USER = '/Users' / MACOS_USER / 'Library/Application Support/Blender' / version_string
    SYSTEM = pathlib.Path('/Library/Application Support/Blender/' + version_string)
else:
    # I only did the 3 most common platforms.  If you want others, add more elif blocks
    # to set USER and SYSTEM  Most Unix systems will work the same as linux
    pass


ADDONS = USER / 'addons'

# Alternate version
# be warned that LOCAL gives a wrong answer
LOCAL = pathlib.Path(bpy.utils.resource_path('LOCAL'))
USER  = pathlib.Path(bpy.utils.resource_path('USER'))
SYSTEM = pathlib.Path(bpy.utils.resource_path('SYSTEM'))

