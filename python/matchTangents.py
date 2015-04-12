# Python code
import math
import maya.cmds as mc
import maya.OpenMaya as om

'''
match('start')
match('end')
'''


def match(data):
    state = data in {'start': True, 'end': False}
    s = mc.playbackOptions(query=True, min=state, max=not state)
    e = mc.playbackOptions(query=True, max=state, min=not state)
    animcurves = mc.keyframe(query=True, name=True)
    tangent = []
    print animcurves
    if animcurves and len(animcurves):
        for curve in animcurves:
            tangent = [mc.keyTangent(curve, query=True, time=(s, s), outAngle=state, inAngle=not state)[0],
                       mc.keyTangent(curve, query=True, time=(e, e), outAngle=state, inAngle=not state)[0]]
            mc.keyTangent(curve, edit=True, lock=False, time=(e, e),
                          outAngle=tangent[state], inAngle=tangent[not state])
    else:
        print "no anim curves found"


