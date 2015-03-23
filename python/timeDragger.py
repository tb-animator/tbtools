import maya.cmds as cmds
import maya.mel as mel

'''
    #hotkey pressed
    import timeDragger as td
    reload(td)
    td.drag("on")
    #hotkey released
    import timeDragger as td
    reload(td)
    td.drag("off")
'''

def drag(str):
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
    if str == "on" :
        mel.eval('storeLastAction( "restoreLastContext " + `currentCtx` )')
        cmds.timeControl(aPlayBackSliderPython,edit = True, snap = False )
        cmds.setToolTo ('TimeDragger')
    elif str == "off":
        #theTime = int(cmds.currentTime( query=True ) )
        cmds.timeControl(aPlayBackSliderPython,edit = True, snap = True )
        cmds.currentTime ( int ( cmds.currentTime(query=True) ) , edit=True )
        mel.eval('invokeLastAction')