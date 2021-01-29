import maya.api.OpenMaya as om2
import maya.cmds as cmds
import apps.callbacks.callbackManager as cbm
import pymel.core as pm

controlLinkAttr = 'link'


def connect_message(source="", destination="", attribute=""):
    add_message(source=destination, attribute=attribute)
    msg_attr = pm.Attribute('%s.%s' % (destination, attribute))
    pm.connectAttr(source + '.message', msg_attr)


def add_message(source="", attribute=""):
    if not pm.attributeQuery(attribute, node=source, exists=True):
        pm.addAttr(source, longName=attribute, at='message')
    return pm.Attribute(source + '.' + attribute)


def addPivotCallbackAttributes(control, pivot):
    control = pm.PyNode(control)
    pivot = pm.PyNode(pivot)
    add_message(control, controlLinkAttr)
    connect_message(control, pivot, controlLinkAttr)


def pivotControlKeyCB(control):
    print 'need to key the control::', control
    cmds.setKeyframe(str(control) + '.rotatePivot')  # , inTangentType='linear', outTangentType='linear')
    return
    cmds.setKeyframe(str(control) + '.translate')


def pivotCallback(msg, plug1, plug2, payload):
    keyCallbackID = '_pivotKey'
    if msg == 2052:
        # 'idle'
        return
    if msg == 18433:
        print 'key added'
        this_mfn_dep = om2.MFnDependencyNode(plug1.node())
        # cmds.cutKey(this_mfn_dep.name())
    if msg == 18434:
        print 'key deleted'
    if msg != 2056:  # edit event
        return

    this_mfn_dep = om2.MFnDependencyNode(plug1.node())
    controlPlug = this_mfn_dep.findPlug("link", False)

    if not controlPlug:
        return
    if not controlPlug.isConnected:
        return

    controlNode = controlPlug.source().node()
    controlDagPath = om2.MDagPath.getAPathTo(controlNode)

    cbManager = cbm.tbCallbackManager()
    ID = str(controlDagPath) + keyCallbackID
    if ID not in cbManager.idleCallbackFunctions.keys():
        print 'pivotCallback adding key callback to idle manager', ID
        x = str(controlDagPath)
        cbManager.addFunctionToIdleScriptJob(ID, lambda: pivotControlKeyCB(x), repeatCount=1, repeatInterval=100)

    control_mfn_dep = om2.MFnDependencyNode(controlNode)
    control_MTransform = om2.MFnTransform(controlDagPath)

    pivotNode = plug1.node()
    pivotDagPath = om2.MDagPath.getAPathTo(pivotNode)
    pivotMTransform = om2.MFnTransform(pivotDagPath)
    pivotRotatePivot = om2.MPoint(pivotMTransform.rotatePivot(om2.MSpace.kWorld))

    translateNames = ['tx', 'ty', 'tz']  # , 'rx','ry', 'rz', 'sx', 'sy', 'sz', ]
    translatePlugs = [control_mfn_dep.findPlug(eachName, False) for eachName in translateNames]
    controlPivot = om2.MPoint(control_MTransform.rotatePivot(om2.MSpace.kWorld))
    control_MTransform.setRotatePivot(pivotRotatePivot, om2.MSpace.kWorld, True)
    rotatePivotTranslateNames = ['rotatePivotTranslateX', 'rotatePivotTranslateY',
                                 'rotatePivotTranslateZ']  # , 'rx','ry', 'rz', 'sx', 'sy', 'sz', ]
    rotatePivotTranslate = [control_mfn_dep.findPlug(eachName, False) for eachName in rotatePivotTranslateNames]
    rptValues = [p.asFloat() for p in rotatePivotTranslate]
    for index, plug in enumerate(translatePlugs):
        plug.setFloat(plug.asFloat() + rptValues[index])
        rotatePivotTranslate[index].setFloat(0.0)

    '''
    cmds.xform(control_mfn_dep.name(), rotatePivot=(float(pivotRotatePivot.x),
                                         float(pivotRotatePivot.y),
                                         float(pivotRotatePivot.z)),
                                         preserve=True, 
                                         worldSpace=True)
    '''


# not used - handle via idle scriptJob
def removeDragCallback():
    global dragCallback
    try:
        if not isinstance(dragCallback, list):
            dragCallback = [dragCallback]
        for cb in dragCallback:
            om2.MEventMessage.removeCallback(cb)
    except:
        pass


def addPivotCallback():
    cbManager = cbm.tbCallbackManager()
    for eachMob in cbManager.iterSelection():
        cbManager.removeCallbacksFromNode(eachMob)
        om2.MNodeMessage.addAttributeChangedCallback(eachMob, pivotCallback)
