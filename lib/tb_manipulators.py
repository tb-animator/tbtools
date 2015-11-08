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

import pymel.core as pm
import maya.cmds as cmds
# from tb_optionVars import optionVar_utils
import tb_optionVars as tb_optionVars
import tb_messages as message

reload(message)
reload(tb_optionVars)


class manips():
    def __init__(self):
        # translation
        self.translate_modes = ['Object', 'Local', 'World', 'Normal',
                                'RotationAxis', 'LiveAxis', 'CustomAxis']
        self.translate_optionVar = "tb_cycle_translation"
        self.translate_messageVar = "tb_cycle_translation_msg_pos"
        self.translate_messageLabel = "message position"

        # rotation
        self.rotate_modes = ['Local', 'World', 'Gimbal']
        self.rotate_optionVar = "tb_cycle_rotation"
        self.rotate_messageVar = "tb_cycle_rotation_msg_pos"
        self.rotate_messageLabel = "message position"

        # selection mask
        self.selection_modes = ['Controls', 'All']
        self.selection_optionVar = "tb_cycle_selection"
        self.rotate_messageVar = "tb_cycle_selection_msg_pos"

        # key types
        self.key_modes = ["spline", "linear", "clamped", "step", "flat", "plateau", "auto"]
        self.key_optionVar = "tb_cycle_keytype"
        self.key_messageVar = "tb_cycle_keytype_msg_pos"
        self.key_messageLabel = "message position"

        if not pm.optionVar(exists='tb_cycle_translation'):
            pm.optionVar(stringValueAppend=(self.translate_optionVar, 'World'))
        pass

    def set_optionVars(self):
        if not pm.optionVar(exists=self.translate_optionVar):
            pass

    def cycleRotation(self):
        '''
        cycleRotation()
        '''
        # get the name of the move type
        cmds.RotateTool()
        rotateMode = cmds.manipRotateContext('Rotate', query=True, mode=True)
        new_mode, new_name = tb_optionVars.optionVar_utils.cycleOption(option_name=self.rotate_optionVar,
                                                                       full_list=self.rotate_modes,
                                                                       current=rotateMode,
                                                                       default='Local'
                                                                       )

        pm.manipRotateContext('Rotate', edit=True, mode=new_mode)
        if pm.optionVar.get(self.rotate_optionVar + "_msg", 0):
            message.info(prefix='rotate',
                         message=' : %s' % new_name,
                         position=pm.optionVar.get(self.rotate_messageVar, 'midCenter')
                         )

    def cycleTranslation(self):
        """
        Translate mode:
        0 - Object Space
        1 - Local Space
        2 - World Space (default)
        3 - Move Along Vertex Normal
        4 - Move Along Rotation Axis
        5 - Move Along Live Object Axis
        6 - Custom Axis Orientation
        """
        cmds.MoveTool()
        move_mode = cmds.manipMoveContext('Move', query=True, mode=True)
        print
        "current,", move_mode
        # get the name of the move type
        new_mode, new_name = tb_optionVars.optionVar_utils.cycleOption(option_name=self.translate_optionVar,
                                                                       full_list=self.translate_modes,
                                                                       current=move_mode,
                                                                       default='World'
                                                                       )

        pm.manipMoveContext('Move', edit=True, mode=new_mode)
        if pm.optionVar.get(self.translate_optionVar + "_msg", 0):
            message.info(prefix='translate',
                         message=' : %s' % new_name,
                         position=pm.optionVar.get(self.translate_messageVar, 'midCenter')
                         )

    # this cycle tool doesn't bother with options yet, just toggles between 2 states
    def cycle_selection_mask(self):
        _mode = pm.selectType(query=True, polymesh=True)

        pm.selectType(allObjects=not _mode)

        if _mode:
            cmds.selectType(joint=_mode, nurbsCurve=_mode)
        pm.selectMode(object=True)

        message.info(prefix='masking',
                     message=' : %s' % self.selection_modes[_mode],
                     position=pm.optionVar.get(self.translate_messageVar, 'midCenter')
                     )

    def cycle_key_type(self):
        _current_key_type = pm.keyTangent(g=True, query=True, outTangentType=True)[0]
        print "current", str(_current_key_type)
        print self.key_modes
        print self.key_modes.index(_current_key_type)

        new_mode, new_name = tb_optionVars.optionVar_utils.cycleOption(option_name=self.key_optionVar,
                                                                       full_list=self.key_modes,
                                                                       current=self.key_modes.index(_current_key_type),
                                                                       default='spline'
                                                                       )
        print "new", new_mode, "name", new_name
        if new_name == "step":
            _in = 'spline'
        else:
            _in = new_name
        _out = new_name

        display_message = 'default spline tangents'
        cmds.keyTangent(g=True, edit=True, inTangentType=_in, outTangentType=_out)
        message.info(prefix='key type',
                     message=' : %s' % _out,
                     position=pm.optionVar.get(self.key_messageVar, 'midCenter')
                     )
