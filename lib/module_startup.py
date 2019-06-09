__author__ = 'Tom'
import maya.cmds as cmds
import maya.utils as mutils
import tb_optionVars as tbo
import pymel.core as pm
import maya.api.OpenMaya as Om
import tb_keyCommands as tb_hotKeys
#import apps.mayaMod.mayaModLoader as mml
import updater as upd
reload(tb_hotKeys)
import maya.mel as mel


class initialise():
    def __init__(self):
        pass

    def check_for_updates(self):
        upd.updater().check_version()
    '''
    def dagLoad(self, *args):
        try:
            mml.customDagLoader().load()
            print "re loading dag menu override"
        except Exception as e:
            print "BAD CALLBACK", Exception, e
    '''
    def load_everything(self):
        tb_hotKeys.hotkey_tool().update_commands()
        tb_hotKeys.hotkey_tool().remove_bad_commands()
        if tbo.set_default_values():
            pm.optionVar(intValue=('tb_firstRun', 0))

        mutils.executeDeferred('import tb_menu as tb_menu;tb_menu.make_ui()')
        mutils.executeDeferred('import updater as upd;upd.updater().check_version()')
        mutils.executeDeferred('import tb_graphEditor as ge;ge.graphEditor().add_graph_editor_callback()')

        # load dag menu edit
        #mutils.executeDeferred('import apps.mayaMod.mayaModLoader as mml;mml.customDagLoader().load()')
        #mutils.executeDeferred('mel.eval(\'scriptJob -conditionTrue \"SomethingSelected\" updateTumble\')')
        #mutils.executeDeferred('mel.eval(\'scriptJob -event \"DragRelease\" updateTumble\')')
        #mutils.executeDeferred('mel.eval(\'scriptJob -event \"ModelPanelSetFocus\" updateTumble\')')
        #mutils.executeDeferred('mel.eval(\'scriptJob -event \"playbackModeChanged\" updateTumble\')')
        #Om.MSceneMessage.addCallback(6, self.dagLoad)
