'''
timeDragger 1.0			
29/03/2015
Tom Bailey				

'''

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import webbrowser
try:
    import tb_messages as message
    from tb_timeline import timeline
except ImportError:
    webbrowser.open('http://tb-animator.blogspot.co.uk/p/hello.html')
    print "please install the tbtools module, it's useful! and required to run this script"

class timeDragger():
    def __init__(self):
        print "look im reloading"
        self.messagePos = "tb_timedrag_msg_pos"
        self.messageVar = "tb_timedrag_msg"
        self.optionVar = "tb_timedrag"
        self.modes = ['toggleBackground']
        self.step_modes = ['odd frames only']
        self.step_label = '    step frames : '
        self.step_var = "tb_timedrag_step_frame"
        self.step_optionVar = "tb_step_odd"
        self.MessagePos = None
        self.showMessage = None
        self.toggle_background = None
        self.update_options()
        self.background_state = cmds.displayPref(query=True, displayGradient=True)
        self.previous_tool = self.get_previous_ctx()
        self.aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
        self.failsafe = None
        self.step_ctx = "what the hell"
        self.step_ctx = pm.draggerContext(name='step_ctx',
                                          pressCommand=self.step_drag_press,
                                          dragCommand=self.step_drag_dragged,
                                          #releaseCommand=self.step_drag_released,
                                          cursor='hand')
        self.start_time = pm.getCurrentTime()
        self.dragPosition = []
        self.pressPosition = []
        self.step = pm.optionVar.get("tb_step_size", 2)
        self.even_only = pm.optionVar.get("tb_step_even", True)
        # for maya 2016 dag evaluation madness
        self.evaluate_mode = ""

    # in case you change the options mid session
    def update_options(self):
        self.MessagePos = pm.optionVar.get(self.messagePos, 'topLeft')
        self.showMessage = pm.optionVar.get(self.messageVar, 0)
        self.toggle_background = pm.optionVar.get(self.optionVar, 0)

    def get_previous_ctx(self):
        if pm.currentCtx() == "TimeDragger" or pm.currentCtx() == "step_ctx":
            previous_tool = 'selectSuperContext'
        else:
            previous_tool = pm.currentCtx()
        return previous_tool

    def drag(self, state):
        self.update_options()
        print self.get_previous_ctx()
        print "state", state
        cmds.timeControl(self.aPlayBackSliderPython, edit=True, snap=not state)
        if state:
            mel.eval('storeLastAction("restoreLastContext ' + self.get_previous_ctx() + '")')
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


    def stepDrag(self, state=True):
        if state:
            try:
                # disable the parallel processing (crashes a lot in 2016)
                self.evaluate_mode = cmds.evaluationManager(mode='off')
            except:
                pass
            self.step = pm.optionVar.get(self.step_var, 2)
            self.even_only = pm.optionVar.get(self.step_optionVar, True)
            print "step even", self.even_only
            cmds.setToolTo(self.step_ctx)
        else:
            mel.eval('invokeLastAction')
            # stepped scrub bypasses evaluation manager as hardly anything in 2016 is thread safe
            try:
                if cmds.evaluationManager(query=True, enabled=True):
                    cmds.evaluationManager(mode=str(self.evaluate_mode))
            except:
                pass

    # Procedure called on press
    def step_drag_press(self):
        self.pressPosition = pm.draggerContext(self.step_ctx, query=True, anchorPoint=True)
        self.start_time = pm.getCurrentTime()

    # Procedure called on drag
    def step_drag_dragged(self):
        self.dragPosition = pm.draggerContext(self.step_ctx, query=True, dragPoint=True)
        distance = self.dragPosition[0] - self.pressPosition[0]
        step_destination = self.start_time + int(distance * 0.05) * self.step
        if self.even_only:
            # snap to odd frames only
            step_destination = int(step_destination/2)*2+1

        pm.setCurrentTime(max(timeline().get_min(), min(step_destination, timeline().get_max())))

    def step_drag_released(self):
        mel.eval('invokeLastAction')

    # this should reset the drag state when the tool is changed, in case you press alt or the windows key when dragging
    def failsafe_scriptjob(self):
        return pm.scriptJob(runOnce=True, event=['ToolChanged', 'my_td.warn();my_td.drag(False)'])

    def info(self):
        print "toggle background :", self.toggle_background
        print "background state  :", self.background_state
        print "previous tool     :", self.previous_tool