'''
timeDragger 1.0			
29/03/2015
Tom Bailey				

'''

import maya.cmds as cmds
import maya.mel as mel

'''
    #hotkey pressed
    import timeDragger as td
    td.drag(True)
    #hotkey released
    import timeDragger as td
    td.drag(False)
'''

def drag(state):
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
    if state:
        mel.eval('storeLastAction("restoreLastContext " + `currentCtx`)')
        cmds.timeControl(aPlayBackSliderPython, edit=True, snap=False )
        cmds.displayPref(displayGradient=False)
        cmds.setToolTo('TimeDragger')
    else:
        #theTime = int(cmds.currentTime(query=True))
        cmds.timeControl(aPlayBackSliderPython, edit=True, snap=True)
        cmds.currentTime(int(cmds.currentTime(query=True)), edit=True)
        cmds.displayPref(displayGradient=True)
        mel.eval('invokeLastAction')
