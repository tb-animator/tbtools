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

    usage - to automatically add a bunch of commands for hotkeys

    from tb_manipulators import manips
    manips.cycleRotation()
    manips.cycleTranslation()
    manips.cycle_selection_mask()

    manips.cycle_key_type()

*******************************************************************************
'''


import maya.cmds as cmds

class manips():
    def __init__(self):
        pass

    @staticmethod
    def cycleRotation():
        '''
        cycleRotation()
        '''
        cmds.RotateTool()
        display_message = ''
        rotateMode = cmds.manipRotateContext('Rotate', query=True, mode=True)
        if rotateMode == 0:
            display_message = 'world'
            cmds.manipRotateContext('Rotate', edit=True, mode=1)
        elif rotateMode == 1:
            display_message = 'gimbal'
            cmds.manipRotateContext('Rotate', edit=True, mode=2)
        elif rotateMode == 2:
            display_message = 'local'
            cmds.manipRotateContext('Rotate', edit=True, mode=0)
        else:
            # cmds.headsUpMessage("Local")
            cmds.manipRotateContext('Rotate', edit=True, mode=0)
        cmds.inViewMessage(amg='rotate <hl>%s</hl>' % display_message,
                           pos='midCenter',
                           fadeStayTime=0.5,
                           fadeOutTime=2.0,
                           fade=True)

    @staticmethod
    def cycleTranslation():
        cmds.MoveTool()
        move_mode = cmds.manipMoveContext('Move', query=True, mode=True)
        if move_mode == 4:
            display_message = 'World'
            _mode = 2
        elif move_mode == 2:
            display_message = 'Local'
            _mode = 1
        elif move_mode == 1:
            display_message = 'Object'
            _mode = 4
        else:
            display_message = 'World'
            _mode = 2
        cmds.manipMoveContext('Move', edit=True, mode=_mode)
        cmds.inViewMessage(amg='translate <hl>%s</hl>' % display_message,
                           pos='midCenter',
                           fadeStayTime=0.5,
                           fadeOutTime=2.0,
                           fade=True)

    @staticmethod
    def cycle_selection_mask():
        _mode = cmds.selectType(query=True, polymesh=True)
        display_message = ['all', 'controls']
        print _mode

        cmds.selectType(allObjects=not _mode)
        if _mode:
            cmds.selectType(joint=_mode, nurbsCurve=_mode)
        cmds.selectMode(object=True)
        cmds.inViewMessage(amg='masking <hl>%s</hl>' % display_message[_mode],
                           pos='midCenter',
                           fadeStayTime=0.5,
                           fadeOutTime=2.0,
                           fade=True)

    @staticmethod
    def cycle_key_type():
        _key_types = []

        if cmds.optionVar(query='NT_tan_spline'):
            _key_types.append("spline")
        if cmds.optionVar(query='NT_tan_linear'):
            _key_types.append("linear")
        if cmds.optionVar(query='NT_tan_clamped'):
            _key_types.append("clamped")
        if cmds.optionVar(query='NT_tan_stepped'):
            _key_types.append("step")
        if cmds.optionVar(query='NT_tan_flat'):
            _key_types.append("flat")
        if cmds.optionVar(query='NT_tan_plateau'):
            _key_types.append("plateau")
        if cmds.optionVar(query='NT_tan_auto'):
            _key_types.append("auto")
        print _key_types
        _current_key_type = cmds.keyTangent(g=True, query=True, outTangentType=True)
        print _current_key_type
        if _current_key_type[0] in _key_types:
            _current_key_index = _key_types.index(_current_key_type[0])
        else:
            print _current_key_type, 'not in list'
            _current_key_index = 0

        if _current_key_index >= len(_key_types) - 1:
            _current_key_index = 0
        else:
            _current_key_index += 1
        _new_key_type = _key_types[_current_key_index]
        print "hello im the key type", _new_key_type
        if _new_key_type == "spline":
            _in = "spline"
            _out = "spline"
            display_message = 'spline tangents'
        elif _new_key_type == "auto":
            _in = "auto"
            _out = "auto"
            display_message = 'auto tangents'
        elif _new_key_type == "step":
            _in = "spline"
            _out = "step"
            display_message = 'step tangents'
        elif _new_key_type == "clamped":
            _in = "clamped"
            _out = "clamped"
            display_message = 'clamped tangents'
        elif _new_key_type == "linear":
            _in = "linear"
            _out = "linear"
            display_message = 'step tangents'
        elif _new_key_type == "plateau":
            _in = "plateau"
            _out = "plateau"
            display_message = 'plateau tangents'
        elif _new_key_type == "flat":
            _in = "flat"
            _out = "flat"
            display_message = 'flat tangents'
        else:
            _in = "spline"
            _out = "spline"
            display_message = 'default spline tangents'
        cmds.keyTangent(g=True, edit=True, inTangentType=_in, outTangentType=_out)
        cmds.inViewMessage(amg='key type <hl>%s</hl>' % _current_key_type[0],
                           pos='midCenter',
                           fadeStayTime=0.5,
                           fadeOutTime=2.0,
                           fade=True)
