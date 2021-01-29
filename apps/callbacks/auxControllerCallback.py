import maya.api.OpenMaya as om2
import maya.cmds as cmds
import apps.callbacks.callbackManager as cbm
import pymel.core as pm

controlLinkAttr = 'link'
constraintLinkAttr = 'constraintLink'
controlOffsetNodeAttr = 'controlOffsetLink'
auxConstraintLinkAttr = 'auxControlConstraintLink'


def connect_message(source="", destination="", attribute=""):
    add_message(source=destination, attribute=attribute)
    msg_attr = pm.Attribute('%s.%s' % (destination, attribute))
    pm.connectAttr(source + '.message', msg_attr)


def add_message(source="", attribute=""):
    if not pm.attributeQuery(attribute, node=source, exists=True):
        pm.addAttr(source, longName=attribute, at='message')
    return pm.Attribute(source + '.' + attribute)


def addAuxCallbackAttributes(control, aux, auxDriver):
    control = pm.PyNode(control)
    aux = pm.PyNode(aux)
    offsetNode = pm.createNode('transform', name=str(control) + '_' + aux + '_offset')
    pm.parent(offsetNode, aux)
    auxConstraint = pm.parentConstraint(auxDriver, aux, maintainOffset=True)
    offsetConstraint = pm.parentConstraint(control, offsetNode)
    connect_message(control, aux, controlLinkAttr)
    connect_message(offsetNode, aux, controlOffsetNodeAttr)
    connect_message(auxConstraint, aux, auxConstraintLinkAttr)
    connect_message(offsetConstraint, aux, constraintLinkAttr)


def auxControlKeyCB(control, cacheID, constraintPlugs):
    cmds.undoInfo(openChunk=True)
    print 'need to key the control::', control
    cbManager = cbm.tbCallbackManager()
    # cbManager.cachedNodes.pop(cacheID)
    for plug in constraintPlugs:
        # plug.setShort(0)
        cmds.setAttr(str(plug), 0)
        print 'plug', plug, 'reset'
    pm.Callback(deferredKey, str(control))
    cbManager.cachedNodes[cacheID].isValid = False
    cbManager.addFunctionToIdleScriptJob('recacheNodes', cbManager.cacheAllNodes, repeatCount=1, repeatInterval=100)
    cmds.undoInfo(closeChunk=True)
    '''
    cmds.setKeyframe(str(control) + '.translate')
    cmds.setKeyframe(str(control) + '.rotate')
    cmds.refresh(force=True)
    cmds.evaluationManager(mode="parallel")
    '''


def refreshAuxControlsPostControlUpdated(control):
    print 'about to refresh all aux controls', control
    cbManager = cbm.tbCallbackManager()
    cbManager.disableAllCallbacks = True
    cbManager.cacheAllNodes()

    cbManager.disableAllCallbacks = False


def deferredKey(control):
    cmds.setKeyframe(str(control) + '.translate')
    cmds.setKeyframe(str(control) + '.rotate')
    cmds.refresh(force=True)
    cmds.evaluationManager(mode="parallel")


def getTransformMatrixPlug(mfnDep):
    return mfnDep.findPlug('worldMatrix', False).elementByLogicalIndex(0)


def auxCallback(msg, plug1, plug2, payload):
    cbManager = cbm.tbCallbackManager()
    if cbManager.disableAllCallbacks:
        return
    keyCallbackID = '_auxKey'
    cacheStateCallbackID = '_cacheState'
    thisDagPath = om2.MDagPath.getAPathTo(plug1.node())
    cacheID = str(thisDagPath) + cacheStateCallbackID
    cmds.evaluationManager(mode="off")
    if msg == 2052:
        # 'idle'
        # on idle event ( effector is selected)
        # cache the offset and send it to the callback manager
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
    controlPlug = this_mfn_dep.findPlug(controlLinkAttr, False)
    auxConstraintPlug = this_mfn_dep.findPlug(auxConstraintLinkAttr, False)
    offsetConstraintPlug = this_mfn_dep.findPlug(constraintLinkAttr, False)
    controlOffsetNodePlug = this_mfn_dep.findPlug(controlOffsetNodeAttr, False)

    if not controlPlug:
        return
    if not controlPlug.isConnected:
        return

    if not auxConstraintPlug:
        return
    if not auxConstraintPlug.isConnected:
        return

    if not offsetConstraintPlug:
        return
    if not offsetConstraintPlug.isConnected:
        return

    if not controlOffsetNodePlug:
        return
    if not controlOffsetNodePlug.isConnected:
        return

    # main control
    controlNode = controlPlug.source().node()
    controlDagPath = om2.MDagPath.getAPathTo(controlNode)

    # the constraint pinning the aux control to the rig
    auxConstraintNode = auxConstraintPlug.source().node()
    auxConstraintDagPath = om2.MDagPath.getAPathTo(auxConstraintNode)

    # constraint getting the offset to the main control
    offsetConstraintNode = offsetConstraintPlug.source().node()
    offsetConstraintDagPath = om2.MDagPath.getAPathTo(offsetConstraintNode)

    # node constrained to main control as offset
    controlOffsetNode = controlOffsetNodePlug.source().node()
    controlOffsetDagPath = om2.MDagPath.getAPathTo(controlOffsetNode)

    control_mfn_dep = om2.MFnDependencyNode(controlNode)
    control_MTransform = om2.MFnTransform(controlDagPath)

    controlOffset_mfn_dep = om2.MFnDependencyNode(controlOffsetNode)
    controlOffset_MTransform = om2.MFnTransform(controlOffsetDagPath)

    auxConstraint_mfn_dep = om2.MFnDependencyNode(auxConstraintNode)
    offsetConstraint_mfn_dep = om2.MFnDependencyNode(offsetConstraintNode)

    # turn off constraints
    offsetConstraintStatePlug = auxConstraint_mfn_dep.findPlug('nodeState', False)
    auxConstraintStatePlug = offsetConstraint_mfn_dep.findPlug('nodeState', False)

    # cbManager = cbm.tbCallbackManager()
    ID = str(controlDagPath) + keyCallbackID
    if ID not in cbManager.idleCallbackFunctions.keys():
        print 'pivotCallback adding key callback to idle manager', ID
        x = str(controlDagPath)
        constraintPlugs = [offsetConstraintStatePlug, auxConstraintStatePlug]
        cbManager.addFunctionToIdleScriptJob(ID, lambda: auxControlKeyCB(x, str(thisDagPath), constraintPlugs),
                                             repeatCount=1,
                                             repeatInterval=100)

    offsetConstraintStatePlug.setShort(2)
    auxConstraintStatePlug.setShort(2)

    controlMatrixPlug = control_mfn_dep.findPlug('worldMatrix', False).elementByLogicalIndex(0)
    controlParentInverseMatrixPlug = control_mfn_dep.findPlug('parentInverseMatrix', False).elementByLogicalIndex(0)
    offsetMatrixPlug = controlOffset_mfn_dep.findPlug('worldMatrix', False).elementByLogicalIndex(0)
    auxMatrixPlug = this_mfn_dep.findPlug('worldMatrix', False).elementByLogicalIndex(0)

    controlMMatrix = om2.MFnMatrixData(controlMatrixPlug.asMObject()).matrix()
    controlTransformMatrixObj = om2.MTransformationMatrix(controlMMatrix)

    controlParentInverseMMatrix = om2.MFnMatrixData(controlParentInverseMatrixPlug.asMObject()).matrix()
    controlParentInverseTransformMatrixObj = om2.MTransformationMatrix(controlParentInverseMMatrix)

    offsetMMatrix = om2.MFnMatrixData(offsetMatrixPlug.asMObject()).matrix()
    offsetTransformMatrixObj = om2.MTransformationMatrix(offsetMMatrix)

    auxMMatrix = om2.MFnMatrixData(auxMatrixPlug.asMObject()).matrix()
    auxTransformMatrixObj = om2.MTransformationMatrix(auxMMatrix)

    # resultMatrix = offsetTransformMatrixObj.asMatrix() * controlParentInverseTransformMatrixObj.asMatrix()
    #
    resultMatrix = cbManager.cachedNodes[str(
        thisDagPath)].localMatrix * auxTransformMatrixObj.asMatrix() * controlParentInverseTransformMatrixObj.asMatrix()
    transformMatrixObj = om2.MTransformationMatrix(resultMatrix)
    translation = transformMatrixObj.translation(om2.MSpace.kWorld)
    rotation = transformMatrixObj.rotation(asQuaternion=False)
    # translation = resultMatrix.translation(om2.MSpace.kWorld)

    translateNames = ['tx', 'ty', 'tz']  # , 'rx','ry', 'rz', 'sx', 'sy', 'sz', ]
    translatePlugs = [control_mfn_dep.findPlug(eachName, False) for eachName in translateNames]
    rotateNames = ['rotateX', 'rotateY', 'rotateZ']
    rotatePlugs = [control_mfn_dep.findPlug(eachName, False) for eachName in rotateNames]

    for index, plug in enumerate(translatePlugs):
        plug.setFloat(translation[index])
    for index, plug in enumerate(rotatePlugs):
        plug.setFloat(rotation[index])

    return

    translateNames = ['translate', 'translateX', 'translateY', 'translateZ']
    rotateNames = ['rotate', 'rotateX', 'rotateY', 'rotateZ']
    attr = plug1.name().split('.')[-1]
    if attr in translateNames:
        print 'translating'

    if attr in rotateNames:
        print 'rotating'

    return True
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


def addAuxCallback():
    cbManager = cbm.tbCallbackManager()
    for eachMob in cbManager.iterSelection():
        cbManager.removeCallbacksFromNode(eachMob)
        om2.MNodeMessage.addAttributeChangedCallback(eachMob, auxCallback)
        dagPath = om2.MDagPath.getAPathTo(eachMob)

        cbManager.addCachedNode(str(dagPath), eachMob)


def controllerCallback(msg, plug1, plug2, payload):
    """
    After the controller has moved, add an idle callback to recache the connected aux controls
    :param msg:
    :param plug1:
    :param plug2:
    :param payload:
    :return:
    """
    cbManager = cbm.tbCallbackManager()
    if cbManager.disableAllCallbacks:
        return
    CallbackID = '_updatedKey'
    cacheStateCallbackID = '_cacheState'
    thisDagPath = om2.MDagPath.getAPathTo(plug1.node())
    cacheID = str(thisDagPath) + cacheStateCallbackID
    # cmds.evaluationManager(mode="off")
    if msg == 2052:
        # 'idle'
        # on idle event ( effector is selected)
        # cache the offset and send it to the callback manager
        return

    if msg == 18433:
        print 'key added'
        this_mfn_dep = om2.MFnDependencyNode(plug1.node())
        # cmds.cutKey(this_mfn_dep.name())
    if msg == 18434:
        print 'key deleted'
    if msg != 2056:  # edit event
        return

    ID = str(thisDagPath) + CallbackID
    if ID not in cbManager.idleCallbackFunctions.keys():
        print 'control has moved, need to update aux controls post edit', ID
        x = str(thisDagPath)
        cbManager.addFunctionToIdleScriptJob(ID, lambda: refreshAuxControlsPostControlUpdated(thisDagPath),
                                             repeatCount=1,
                                             repeatInterval=100)
    return


def addControllerCallback():
    cbManager = cbm.tbCallbackManager()
    for eachMob in cbManager.iterSelection():
        cbManager.removeCallbacksFromNode(eachMob)
        om2.MNodeMessage.addAttributeChangedCallback(eachMob, controllerCallback)
        dagPath = om2.MDagPath.getAPathTo(eachMob)
