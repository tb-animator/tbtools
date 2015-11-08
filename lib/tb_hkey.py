'''TB Animation Tools is a toolset for animators

*******************************************************************************
    License and Copyright
    Copyright 2015-Tom Bailey
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    send issues/ requests to brimblashman@gmail.com
    visit tb-animator.blogspot.com for "stuff"

*******************************************************************************
'''

# class for holding hotkey command info
class tb_hkey():
    def __init__(self, name="", annotation="", category="tb_tools", language='python', command=[""]):
        self.name = name
        self.annotation = annotation
        self.category = category
        self.language = language
        self.command = self.collapse_command_list(command)
        
    def collapse_command_list(self, command):
        cmd = ""
        for lines in command:
            cmd = cmd + lines + "\n"
        return cmd