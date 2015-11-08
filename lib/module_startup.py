__author__ = 'Tom'


import maya.utils as mutils
import tb_optionVars as tbo
import pymel.core as pm

import tb_keyCommands as tb_hotKeys
reload(tb_hotKeys)


class initialise():
    def __init__(self):
        pass

    def load_everything(self):
        tb_hotKeys.hotkey_tool().update_commands()
        tb_hotKeys.hotkey_tool().remove_bad_commands()
        if tbo.set_default_values():
            pm.optionVar(intValue=('tb_firstRun', True))
        mutils.executeDeferred('import tb_menu as tb_menu;tb_menu.make_ui()')