'''
timeDragger 1.0			
29/03/2015
Tom Bailey				

'''

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import tb_messages as message
'''
    #hotkey pressed
    import tb_timeDragger as td
    td.drag(True)
    #hotkey released
    import tb_timeDragger as td
    td.drag(False)
'''
class timeDragger():
    def __init__(self):
        self.messagePos =  "tb_timedrag_msg_pos"
        self.messageVar = "tb_timedrag_msg"
        self.optionVar = "tb_timedrag"
        self.modes = ['toggleBackground']
        self.MessagePos = None
        self.showMessage = None
        self.toggle_background = None
        self.update_options()
        self.background_state = cmds.displayPref(query=True, displayGradient=True)
        self.previous_tool = self.get_previous_ctx()
        self.aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
        self.failsafe = None

    # in case you change the options mid session
    def update_options(self):
        self.MessagePos = pm.optionVar.get(self.messagePos, 'topLeft')
        self.showMessage = pm.optionVar.get(self.messageVar, 0)
        self.toggle_background = pm.optionVar.get(self.optionVar, 0)

    def get_previous_ctx(self):
        if pm.currentCtx() == "TimeDragger":
            previous_tool = 'selectSuperContext'
        else:
            previous_tool = pm.currentCtx()
        return previous_tool

    def drag(self, state):
        self.update_options()
        print self.get_previous_ctx()
        print "state", state
        cmds.timeControl(self.aPlayBackSliderPython, edit=True, snap=not state )
        if state:
            mel.eval('storeLastAction("restoreLastContext ' +  self.get_previous_ctx() + '")')
            if self.toggle_background:
                cmds.displayPref(displayGradient=False)
            if self.showMessage:
                msg = 'on'
                message.info(prefix='smooth drag',
                     message=' : %s' % msg,
                     position=self.MessagePos
                     )
            cmds.setToolTo('TimeDragger')
        else:
            if self.showMessage:
                msg = 'off'
                message.info(prefix='smooth drag',
                     message=' : %s' % msg,
                     position=self.MessagePos
                     )
            pm.setCurrentTime(int(pm.getCurrentTime()))
            cmds.displayPref(displayGradient=self.background_state)
            mel.eval('invokeLastAction')


    def warn(self):
        self.failsafe = None
        msg = "you pressed some weird combination of alt or maybe the windows key"
        print msg
        message.error(prefix='Warning',
                     message=' : %s' % msg,
                     position='botRight'
                     )


    # this should reset the drag state when the tool is changed, in case you press alt or the windows key when dragging
    def failsafe_scriptjob(self):
        return pm.scriptJob( runOnce=True, event=['ToolChanged', 'my_td.warn();my_td.drag(False)'])

    def info(self):
        print "toggle background :", self.toggle_background
        print "background state  :", self.background_state
        print "previous tool     :", self.previous_tool