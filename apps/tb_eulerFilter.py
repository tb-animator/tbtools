import maya.cmds as mc

class EulerFilter(object):
    def __init__(self):
        self.objects = mc.ls(selection=True)
        self.selected = False
        # get the min and max times from our keyframe selection
        if mc.keyframe(query=True, selected=True):
            self.firstTime = min(min(mc.keyframe(query=True, selected=True, timeChange=True)),99999999)
            self.lastTime = min(max(mc.keyframe(query=True, selected=True, timeChange=True)),99999999)
            self.selected = True

    def filter(self):
        if self.selected:
            # copy keys to buffer
            mc.selectKey(self.objects, replace=True, time=(self.firstTime, self.lastTime))
            mc.bufferCurve(animation='keys', overwrite=True)
            # delete surrounding keys
            mc.cutKey(self.objects, time=(-9999999,self.firstTime-0.01))
            mc.cutKey(self.objects, time=(self.lastTime+0.01, 999999))
            # euler filter
            mc.filterCurve()
            # copy keys
            mc.copyKey(self.objects, time=(self.firstTime, self.lastTime))
            # swap buffer to original
            mc.bufferCurve(animation='keys', swap=True)
            # paste keys back
            mc.pasteKey(option='merge')
        else:
            mc.filterCurve()

