import maya.api.OpenMaya as om2
import maya.cmds as cmds


def dragReleaseCB(*args):
    sel = iterSelection()
    for node in sel:
        mfn_dep = om2.MFnDependencyNode(node)
        if not mfn_dep.hasAttribute('link'):
            print 'no link attr'
            return

        msgPlug = mfn_dep.findPlug('link', False)
        if not msgPlug:
            return
        if not msgPlug.isConnected:
            print 'no connection', mfn_dep, 'link'
            return

        connectedNode = msgPlug.destinations()
        print 'connectedNode', connectedNode
        if not connectedNode:
            return
        connected_mfn_dep = om2.MFnDependencyNode(connectedNode[0].node())
        # print connected_mfn_dep.name()
        dirtyTracker = connected_mfn_dep.findPlug('isDirty', False)

        if dirtyTracker:
            if dirtyTracker.asBool() == True:
                dirtyTracker.setBool(False)
                constraintPlug = mfn_dep.findPlug("constraint", False)
                if not constraintPlug:
                    return
                if not constraintPlug.isConnected:
                    return

                constraintNode = constraintPlug.source().node()
                constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
                statePlug = constraint_mfn_dep.findPlug('nodeState', False)
                statePlug.setShort(0)

                constraintPlug = mfn_dep.findPlug("offsetConstraint", False)
                if not constraintPlug:
                    return
                if not constraintPlug.isConnected:
                    return

                constraintNode = constraintPlug.source().node()
                constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
                statePlug = constraint_mfn_dep.findPlug('nodeState', False)
                statePlug.setShort(0)


def ikHandleReleaseCB(*args):
    sel = iterSelection()
    for node in sel:
        mfn_dep = om2.MFnDependencyNode(node)
        if not mfn_dep.hasAttribute('constraint'):
            print 'no constraint attr'
            return

        constraintPlug = mfn_dep.findPlug("constraint", False)
        if not constraintPlug:
            print 'no constraint plug'
            return
        if not constraintPlug.isConnected:
            print 'not connected'
            return

        constraintNode = constraintPlug.source().node()
        constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
        statePlug = constraint_mfn_dep.findPlug('nodeState', False)
        statePlug.setShort(0)


def ikReleaseCB(*args):
    sel = iterSelection()
    for node in sel:
        mfn_dep = om2.MFnDependencyNode(node)
        if not mfn_dep.hasAttribute('link'):
            return
        msgPlug = mfn_dep.findPlug('link', False)
        if not msgPlug:
            return

        connectedNode = msgPlug.destinations()
        # print 'connectedNode', connectedNode
        if not connectedNode:
            return
        connected_mfn_dep = om2.MFnDependencyNode(connectedNode[0].node())
        # print connected_mfn_dep.name()
        dirtyTracker = connected_mfn_dep.findPlug('isDirty', False)

        if dirtyTracker:
            if dirtyTracker.asBool() == True:
                dirtyTracker.setBool(False)
                constraintPlug = mfn_dep.findPlug("constraint", False)
                if not constraintPlug:
                    return
                if not constraintPlug.isConnected:
                    return

                constraintNode = constraintPlug.source().node()
                constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
                statePlug = constraint_mfn_dep.findPlug('nodeState', False)
                statePlug.setShort(0)


def iterSelection():
    """
    generator style iterator over current Maya active selection
    :return: [MObject) an MObject for each item in the selection
    """
    sel = om2.MGlobal.getActiveSelectionList()
    for i in xrange(sel.length()):
        yield sel.getDependNode(i)


def removeCallbacksFromNode(node_mob):
    """
    :param node_mob: [MObject] the node to remove all node callbacks from 
    :return: [int] number of callbacks removed
    """
    cbs = om2.MMessage.nodeCallbacks(node_mob)
    for eachCB in cbs:
        om2.MMessage.removeCallback(eachCB)
    len(cbs)


def translationPlugsFromAnyPlug(plug):
    """
    :param plug: [MPlug] plug on a node to retrieve translation related plugs from
    :return: [tuple(MPlug)] tuple of compound translate plug,
                            and three axes translate plugs
    """
    node = plug.node()
    if not node.hasFn(om2.MFn.kTransform):  # this should exclude nodes without translate plugs
        return
    mfn_dep = om2.MFnDependencyNode(node)
    pNames = ('translate', 'tx', 'ty', 'tz')
    return tuple([mfn_dep.findPlug(eachName, False) for eachName in pNames])


def rotationPlugsFromAnyPlug(plug):
    """
    :param plug: [MPlug] plug on a node to retrieve translation related plugs from
    :return: [tuple(MPlug)] tuple of compound translate plug,
                            and three axes translate plugs
    """
    node = plug.node()
    if not node.hasFn(om2.MFn.kTransform):  # this should exclude nodes without translate plugs
        return
    mfn_dep = om2.MFnDependencyNode(node)
    pNames = ('rotate', 'rx', 'ry', 'rz')
    return tuple([mfn_dep.findPlug(eachName, False) for eachName in pNames])


def translationPlugsfromMfnDep(mfn_dep):
    pNames = ('translate', 'tx', 'ty', 'tz')
    return tuple([mfn_dep.findPlug(eachName, False) for eachName in pNames])


def rotationPlugsfromMfnDep(mfn_dep):
    pNames = ('rotate', 'rx', 'ry', 'rz')
    return tuple([mfn_dep.findPlug(eachName, False) for eachName in pNames])


def msgConnectedPlugs(plug):
    """
    :param plug: [MPlug] plug on a node owning message plug
                         we wish to retrieve all destination plugs from
    :return: [tuple(MPlug)] all plugs on other nodes receiving a message connection
                            coming from the one owning the argument plug
    """
    mfn_dep = om2.MFnDependencyNode(plug.node())
    msgPlug = mfn_dep.findPlug('link', False)
    return tuple([om2.MPlug(otherP) for otherP in msgPlug.destinations()])


def almostEqual(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    Lifted from pre 3.5 isclose() implementation,
    floating point error tolerant comparison
    :param a: [float] first number in comparison
    :param b: [float] second number in comparison
    :param rel_tol:  [float] relative tolerance in comparison
    :param abs_tol:  [float] absolute tolerance in case of relative tolerance issues
    :return: [bool] args are equal or not
    """
    return abs(a - b) == max(rel_tol * max(abs(a), abs(b)), abs_tol)


def cb(msg, plug1, plug2, payload):
    if msg != 2056:  # check most common case first and return unless it's
        return  # an attribute edit type of callback

    this_mfn_dep = om2.MFnDependencyNode(plug1.node())
    print 'node', this_mfn_dep
    constraintPlug = this_mfn_dep.findPlug("constraint", False)
    offsetConstraintPlug = this_mfn_dep.findPlug("offsetConstraint", False)

    if not constraintPlug:
        return
    if not constraintPlug.isConnected:
        return

    constraintNode = constraintPlug.source().node()
    constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
    statePlug = constraint_mfn_dep.findPlug('nodeState', False)
    statePlug.setShort(2)

    offsetConstraintNode = offsetConstraintPlug.source().node()
    offsetConstraint_mfn_dep = om2.MFnDependencyNode(offsetConstraintNode)
    statePlug = offsetConstraint_mfn_dep.findPlug('nodeState', False)
    statePlug.setShort(2)

    affectedNodePlug = this_mfn_dep.findPlug("link", False)
    affected_mfn_dep = om2.MFnDependencyNode(affectedNodePlug.source().node())
    print 'affected_mfn_dep', affected_mfn_dep.name
    offsetNodePlug = this_mfn_dep.findPlug("offset", False)
    offset_mfn_dep = om2.MFnDependencyNode(offsetNodePlug.source().node())

    dirtyTrackerPlug = affected_mfn_dep.findPlug('isDirty', False)
    if not dirtyTrackerPlug.asBool():
        dirtyTrackerPlug.setBool(1)

    #
    offsetMMatrix = om2.MMatrix(cmds.xform(offset_mfn_dep.name(), matrix=True, ws=0, q=True))
    thisMMatrix = om2.MMatrix(cmds.xform(this_mfn_dep.name(), matrix=True, ws=1, q=True))

    resultTFMatrix = om2.MTransformationMatrix(offsetMMatrix * thisMMatrix)
    thisTFMatrix = om2.MTransformationMatrix(thisMMatrix)
    print 't:', resultTFMatrix.translation(om2.MSpace.kWorld)
    print 'r:', resultTFMatrix.rotationComponents(asQuaternion=False)

    srcTranslationPlugs = translationPlugsfromMfnDep(affected_mfn_dep)[1:4]
    if not len(srcTranslationPlugs):
        return
    srcRotationPlugs = rotationPlugsfromMfnDep(affected_mfn_dep)[1:4]
    if not len(srcRotationPlugs):
        return

    # trim out the first plug, the translate compound, and only work on the triplet xyz
    ws = resultTFMatrix.translation(om2.MSpace.kWorld)
    resultTranslationValues = [ws.x, ws.y, ws.z]
    resultRotationValues = resultTFMatrix.rotationComponents(asQuaternion=False)
    # values = resultTFMatrix.rotationComponents(asQuaternion=False)
    # print values
    for i, p in enumerate(srcTranslationPlugs):
        print i
        if almostEqual(p.asFloat(), resultTranslationValues[i]):
            continue
        p.setFloat(resultTranslationValues[i])

    for i, p in enumerate(srcRotationPlugs):
        if almostEqual(p.asFloat(), resultRotationValues[i]):
            continue
        p.setFloat(resultRotationValues[i])


def ikHandleCallback(msg, plug1, plug2, payload):
    if msg != 2056:  # check most common case first and return unless it's
        return  # an attribute edit type of callback

    this_mfn_dep = om2.MFnDependencyNode(plug1.node())

    constraintPlug = this_mfn_dep.findPlug("constraint", False)
    if not constraintPlug:
        return
    if not constraintPlug.isConnected:
        return

    constraintNode = constraintPlug.source().node()
    constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
    statePlug = constraint_mfn_dep.findPlug('nodeState', False)
    statePlug.setShort(2)

    jointListPlug = this_mfn_dep.findPlug("jointList", False)

    # get the joints connected to the list
    for index in range(0, jointListPlug.numElements()):
        # get the joint
        joint = jointListPlug.connectionByPhysicalIndex(index).source().node()
        # this joint should have a snap target
        joint_mfnDep = om2.MFnDependencyNode(joint)
        snapTargetPlug = joint_mfnDep.findPlug("ikSnapTarget", False)
        ikJoint = snapTargetPlug.source().node()
        ikJoint_mfnDep = om2.MFnDependencyNode(ikJoint)
        # print joint_mfnDep.name(), ikJoint_mfnDep.name()

        # just get ik target matrix
        ikMMatrix = om2.MMatrix(cmds.xform(ikJoint_mfnDep.name(), matrix=True, ws=0, q=True))
        resultTFMatrix = om2.MTransformationMatrix(ikMMatrix)

        values = resultTFMatrix.rotationComponents(asQuaternion=False)
        # print values

        destRotationPlugs = rotationPlugsfromMfnDep(joint_mfnDep)[1:4]
        for i, p in enumerate(destRotationPlugs):
            if almostEqual(p.asFloat(), values[i]):
                continue
            p.setFloat(values[i])

    return
    constraintPlug = this_mfn_dep.findPlug("constraint", False)
    offsetConstraintPlug = this_mfn_dep.findPlug("offsetConstraint", False)

    if not constraintPlug:
        return
    if not constraintPlug.isConnected:
        return

    constraintNode = constraintPlug.source().node()
    constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
    statePlug = constraint_mfn_dep.findPlug('nodeState', False)
    statePlug.setShort(2)

    '''
    offsetConstraintNode = offsetConstraintPlug.source().node()
    offsetConstraint_mfn_dep = om2.MFnDependencyNode(offsetConstraintNode)
    statePlug = offsetConstraint_mfn_dep.findPlug('nodeState', False)
    statePlug.setShort(2)
    '''

    affectedNodePlug = this_mfn_dep.findPlug("link", False)
    destinations = affectedNodePlug.destinations()
    for dest in destinations:
        affected_mfn_dep = om2.MFnDependencyNode(dest.node())

        ikNodePlug = this_mfn_dep.findPlug("ikJoint", False)
        ik_mfn_dep = om2.MFnDependencyNode(ikNodePlug.source().node())

        dirtyTrackerPlug = affected_mfn_dep.findPlug('isDirty', False)
        if not dirtyTrackerPlug.asBool():
            dirtyTrackerPlug.setBool(1)
        # print affected_mfn_dep.name(), ik_mfn_dep.name()

        ikMMatrix = om2.MMatrix(cmds.xform(ik_mfn_dep.name(), matrix=True, ws=0, q=True))
        thisMMatrix = om2.MMatrix(cmds.xform(ik_mfn_dep.name(), matrix=True, ws=0, q=True))

        resultTFMatrix = om2.MTransformationMatrix(ikMMatrix)
        thisTFMatrix = om2.MTransformationMatrix(thisMMatrix)

        '''
        #print 't:', resultTFMatrix.translation(om2.MSpace.kWorld)
        #print 'r:', resultTFMatrix.rotationComponents(asQuaternion=False)
        srcTranslationPlugs = translationPlugsFromAnyPlug(plug1)
        if not len(srcTranslationPlugs):
            return
     
        # trim out the first plug, the translate compound, and only work on the triplet xyz
        values = [p.asFloat() for p in srcTranslationPlugs[1:4]]
        values = resultTFMatrix.translation(om2.MSpace.kWorld)
    
        for eachDestPlug in msgConnectedPlugs(plug1): # all receiving plugs
            destTranslationPlugs = translationPlugsFromAnyPlug(eachDestPlug)[1:4]
            for i, p in enumerate(destTranslationPlugs):
                if almostEqual(p.asFloat(), values[i]):
                    continue
                #p.setFloat(values[i])
                p.setFloat(values[i])
        '''
        srcRotationPlugs = rotationPlugsFromAnyPlug(plug1)
        if not len(srcRotationPlugs):
            return

        # trim out the first plug, the translate compound, and only work on the triplet xyz
        values = [p.asFloat() for p in srcRotationPlugs[1:4]]
        values = resultTFMatrix.rotationComponents(asQuaternion=False)
        # print values

        for eachDestPlug in msgConnectedPlugs(plug1):  # all receiving plugs
            destRotationPlugs = rotationPlugsFromAnyPlug(eachDestPlug)[1:4]
            for i, p in enumerate(destRotationPlugs):
                if almostEqual(p.asFloat(), values[i]):
                    continue
                p.setFloat(values[i])


def ikPVCallback(msg, plug1, plug2, payload):
    if msg != 2056:  # check most common case first and return unless it's
        return  # an attribute edit type of callback

    this_mfn_dep = om2.MFnDependencyNode(plug1.node())
    constraintPlug = this_mfn_dep.findPlug("constraint", False)
    offsetConstraintPlug = this_mfn_dep.findPlug("offsetConstraint", False)

    if not constraintPlug:
        return
    if not constraintPlug.isConnected:
        return

    constraintNode = constraintPlug.source().node()
    constraint_mfn_dep = om2.MFnDependencyNode(constraintNode)
    statePlug = constraint_mfn_dep.findPlug('nodeState', False)
    statePlug.setShort(2)

    '''
    offsetConstraintNode = offsetConstraintPlug.source().node()
    offsetConstraint_mfn_dep = om2.MFnDependencyNode(offsetConstraintNode)
    statePlug = offsetConstraint_mfn_dep.findPlug('nodeState', False)
    statePlug.setShort(2)
    '''

    affectedNodePlug = this_mfn_dep.findPlug("link", False)
    destinations = affectedNodePlug.destinations()
    for dest in destinations:
        affected_mfn_dep = om2.MFnDependencyNode(dest.node())

        ikNodePlug = this_mfn_dep.findPlug("ikJoint", False)
        ik_mfn_dep = om2.MFnDependencyNode(ikNodePlug.source().node())

        dirtyTrackerPlug = affected_mfn_dep.findPlug('isDirty', False)
        if not dirtyTrackerPlug.asBool():
            dirtyTrackerPlug.setBool(1)
        # print affected_mfn_dep.name(), ik_mfn_dep.name()

        ikMMatrix = om2.MMatrix(cmds.xform(ik_mfn_dep.name(), matrix=True, ws=0, q=True))
        thisMMatrix = om2.MMatrix(cmds.xform(ik_mfn_dep.name(), matrix=True, ws=0, q=True))

        resultTFMatrix = om2.MTransformationMatrix(ikMMatrix)
        thisTFMatrix = om2.MTransformationMatrix(thisMMatrix)

        '''
        #print 't:', resultTFMatrix.translation(om2.MSpace.kWorld)
        #print 'r:', resultTFMatrix.rotationComponents(asQuaternion=False)
        srcTranslationPlugs = translationPlugsFromAnyPlug(plug1)
        if not len(srcTranslationPlugs):
            return
     
        # trim out the first plug, the translate compound, and only work on the triplet xyz
        values = [p.asFloat() for p in srcTranslationPlugs[1:4]]
        values = resultTFMatrix.translation(om2.MSpace.kWorld)
    
        for eachDestPlug in msgConnectedPlugs(plug1): # all receiving plugs
            destTranslationPlugs = translationPlugsFromAnyPlug(eachDestPlug)[1:4]
            for i, p in enumerate(destTranslationPlugs):
                if almostEqual(p.asFloat(), values[i]):
                    continue
                #p.setFloat(values[i])
                p.setFloat(values[i])
        '''
        srcRotationPlugs = rotationPlugsfromMfnDep(ik_mfn_dep)
        if not len(srcRotationPlugs):
            return

        # trim out the first plug, the translate compound, and only work on the triplet xyz
        values = [p.asFloat() for p in srcRotationPlugs[1:4]]
        # values = resultTFMatrix.rotationComponents(asQuaternion=False)
        # print values
        destRotationPlugs = rotationPlugsfromMfnDep(affected_mfn_dep)[1:4]
        for i, p in enumerate(destRotationPlugs):
            if almostEqual(p.asFloat(), values[i]):
                continue
            p.setFloat(values[i])


def removeDragCallback():
    global dragCallback
    try:
        if not isinstance(dragCallback, list):
            dragCallback = [dragCallback]
        for cb in dragCallback:
            om2.MEventMessage.removeCallback(cb)
    except:
        pass


def addPivotDragCallback():
    global dragCallback
    dragCallback = []
    # dragCallback.append(om2.MEventMessage.addEventCallback('DragRelease', ikHandleReleaseCB))
    dragCallback.append(om2.MEventMessage.addEventCallback('DragRelease', dragReleaseCB))


def removePivotCallback():
    for eachMob in iterSelection():
        removeCallbacksFromNode(eachMob)


def addPivotCallback():
    for eachMob in iterSelection():
        removeCallbacksFromNode(eachMob)
        om2.MNodeMessage.addAttributeChangedCallback(eachMob, cb)


def addIKPVCallback():
    for eachMob in iterSelection():
        removeCallbacksFromNode(eachMob)
        om2.MNodeMessage.addAttributeChangedCallback(eachMob, ikPVCallback)


def removeIKCallback():
    for eachMob in iterSelection():
        removeCallbacksFromNode(eachMob)


def addIKHandleCallback():
    for eachMob in iterSelection():
        removeCallbacksFromNode(eachMob)
        om2.MNodeMessage.addAttributeChangedCallback(eachMob, ikHandleCallback)
