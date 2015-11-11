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

    usage


*******************************************************************************
'''

__author__ = 'tom.bailey'
import pymel.core as pm
from tb_objectInfo import mod_panel

class isolator():
    def __init__(self):
        pass

    def toggle_isolate(self):
        '''
        import isolate as iso
        reload (iso)
        iso.isolate()
        '''
        selection = pm.ls(selection=True)
        panel = mod_panel().getModelPanel()

        state = pm.isolateSelect(panel, query=True, state=True)
        if state:
            pm.isolateSelect(panel, state=0)
            pm.isolateSelect(panel, removeSelected=True)
        else:
            pm.isolateSelect(panel, state=1)
            pm.isolateSelect(panel, addSelected=True)