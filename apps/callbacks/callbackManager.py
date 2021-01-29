import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2a
import maya.cmds as cmds
import pymel.core as pm


class tbCallbackManager(object):
    __instance = None

    sceneChangeCallbacks = list()
    idleCallbackFunctions = dict()
    idleCallback = -1
    timeChangedCallback = -1
    selectionChangedCallback = -1
    idleScriptJobPendingDelete = False
    timeSlider = pm.melGlobals['gPlayBackSlider']
    cachedNodes = dict()
    disableAllCallbacks = False

    def __new__(cls, val='default'):
        if tbCallbackManager.__instance is None:
            tbCallbackManager.__instance = object.__new__(cls)
            tbCallbackManager.__instance.createSceneChangedCallback()
            tbCallbackManager.__instance.createMasterTimeChangeCallback()
            tbCallbackManager.__instance.createMasterSelectionChangedCallback()

        tbCallbackManager.__instance.val = val
        return tbCallbackManager.__instance

    def __del__(self):
        print('Destructor called, Callback manager deleted.')

    def remove(self):
        self.killMasterSelectionChangedCallback()
        self.killMasterTimeChangeCallback()
        self.killMasterIdleCallback()

    def createSceneChangedCallback(self):
        """
        Add callbacks to trigger when scene changes
        :return:
        """
        self.sceneChangeCallbacks.append(om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeNew,
                                                                      self.removeAllCallbacks))
        self.sceneChangeCallbacks.append(om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeOpen,
                                                                      self.removeAllCallbacks))

    def removeAllCallbacks(self):
        """
        Remove all callbacks in the scene when changing scene
        :return:
        """
        pass

    def createMasterIdleCallback(self):
        # self.idleCallback = om2.MTimerMessage.addTimerCallback(0.001, self.masterIdleCallbackFunction)
        # self.idleScriptJob = cmds.scriptJob(idleEvent=self.masterIdleScriptJobFunction, runOnce=False)
        self.killMasterIdleCallback()
        self.idleCallback = om2.MEventMessage.addEventCallback('idle', self.masterIdleScriptJobFunction)

    def killMasterIdleCallback(self):
        if self.idleCallback is not -1:
            om2.MEventMessage.removeCallback(self.idleCallback)
            self.idleCallback = -1

    def createMasterSelectionChangedCallback(self, *args):
        self.killMasterSelectionChangedCallback()
        self.selectionChangedCallback = om2.MEventMessage.addEventCallback('SelectionChanged',
                                                                           self.selectionChagedFunction)

    def killMasterSelectionChangedCallback(self):
        if self.selectionChangedCallback is not -1:
            om2.MEventMessage.removeCallback(self.selectionChangedCallback)
            self.selectionChangedCallback = -1

    def createMasterTimeChangeCallback(self):
        self.killMasterTimeChangeCallback()
        self.timeChangedCallback = om2.MEventMessage.addEventCallback('timeChanged', self.timeChangedFunc)

    def killMasterTimeChangeCallback(self):
        if self.timeChangedCallback is not -1:
            om2.MEventMessage.removeCallback(self.timeChangedCallback)
            self.killMasterTimeChangeCallback = -1

    def timeChangedFunc(self, *args):
        if not om2a.MAnimControl.isPlaying():
            if 'recacheNodes' not in self.idleCallbackFunctions.keys():
                self.addFunctionToIdleScriptJob('recacheNodes', self.cacheAllNodes, repeatCount=1, repeatInterval=100)

    def selectionChagedFunction(self, *args):
        animList = cmds.selectionConnection("animationList", query=True, object=True)
        sel = om2.MGlobal.getActiveSelectionList()
        if sel.length() == 1:
            depNode = sel.getDependNode(0)
            mfn_dep = om2.MFnDependencyNode(depNode)
            if not mfn_dep.hasAttribute(controlLinkAttr):
                self.revertTimeSliderSelectionConnection()
                return
            controlPlug = mfn_dep.findPlug(controlLinkAttr, False)
            if not controlPlug:
                self.revertTimeSliderSelectionConnection()
                return
            if not controlPlug.isConnected:
                self.revertTimeSliderSelectionConnection()
                return
            if not controlPlug.isDestination:
                self.revertTimeSliderSelectionConnection()
                return
            controlNodeSource = controlPlug.source()
            if not controlNodeSource:
                self.revertTimeSliderSelectionConnection()
                return
            controlNode = controlNodeSource.node()
            if not controlNode:
                self.revertTimeSliderSelectionConnection()
                return
            controlDagPath = om2.MDagPath.getAPathTo(controlNode)
            self.swapTimeSliderSelectionConnection('auxLink', controlDagPath)
        else:
            self.revertTimeSliderSelectionConnection()
            return

    def stopMasterIdleScriptJob(self):
        print 'removing idle script job'
        '''
        cmds.scriptJob(kill=self.idleScriptJob)
        '''
        try:
            om2.MEventMessage.removeCallback(self.idleCallback)
        except:
            cmds.warning('attempting to remove master callback failing')
        self.idleCallback = -1
        self.idleScriptJobPendingDelete = False

    def masterIdleScriptJobFunction(self, *args):
        if self.idleCallback is -1:
            print 'quitting masterIdleScriptJobFunction as scriptJob has been removed'
            return
        if self.idleScriptJobPendingDelete:
            print 'doing nothing in masterIdleScriptJobFunction as scriptJob is about to be removed'
            return
        if not self.idleCallbackFunctions.items():
            print 'function list now empty, halting idle callback'
            cmds.evalDeferred(self.stopMasterIdleScriptJob)
            self.idleScriptJobPendingDelete = True
            return

        idToRemove = list()
        for ID, callbackData in self.idleCallbackFunctions.items():
            # print ID, callbackData, callbackData.repeatCount
            if callbackData.repeatCount == 0:
                # remove finished callback
                print 'counter expired on ID', ID
                idToRemove.append(ID)
            else:
                if callbackData.repeatCount is not 'infinite':
                    print 'reducing count on ID', ID
                    callbackData.repeatCount = max(0, callbackData.repeatCount - 1)
                print 'calling funciton', callbackData.function
                callbackData.function()
        for id in idToRemove:
            print 'REMOVING ID', id
            self.idleCallbackFunctions.pop(id)

    '''
    def stopMasterIdleCallback(self):
        om2.MMessage.removeCallback(self.idleCallback)

    def masterIdleCallbackFunction(self, elapsedTime, execTime, data):
        for key, value in self.idleCallbackFunctions.items():
            print key, value
        print 'cb func', elapsedTime, execTime, data
    '''

    def addFunctionToIdleScriptJob(self, ID, function, repeatCount='infinite', repeatInterval=100):
        self.idleCallbackFunctions[ID] = IdleCallbackData(ID=ID,
                                                          function=function,
                                                          repeatCount=repeatCount,
                                                          repeatInterval=repeatInterval)
        if self.idleCallback is -1:
            print 'adding new idle scriptJob as a new function has been added to an empty queue'
            self.createMasterIdleCallback()

    def addCachedNode(self, node, node_mob):
        if node in self.cachedNodes.keys():
            return

        if node not in self.cachedNodes.keys():
            print 'caching node', node
            self.cachedNodes[node] = nodeCacheData(node_mob)

    def cacheAllNodes(self):
        print 'cache nodes', self.cachedNodes.keys()
        for node in self.cachedNodes.values():
            node.isValid = False
            node.cacheMatrix()

    def getCachedNode(self, node_mob):
        pass

    @staticmethod
    def iterSelection():
        """
        generator style iterator over current Maya active selection
        :return: [MObject) an MObject for each item in the selection
        """
        sel = om2.MGlobal.getActiveSelectionList()
        for i in xrange(sel.length()):
            yield sel.getDependNode(i)

    @staticmethod
    def removeCallbacksFromNode(node_mob):
        """
        :param node_mob: [MObject] the node to remove all node callbacks from
        :return: [int] number of callbacks removed
        """
        cbs = om2.MMessage.nodeCallbacks(node_mob)
        for eachCB in cbs:
            om2.MMessage.removeCallback(eachCB)
        return len(cbs)

    def revertTimeSliderSelectionConnection(self):
        cmds.timeControl(self.timeSlider, edit=True, mainListConnection='animationList')

    def swapTimeSliderSelectionConnection(self, sc, obj):
        if not cmds.selectionConnection(sc, query=True, exists=True):
            cmds.selectionConnection(sc, object=obj)
        cmds.timeControl(self.timeSlider, edit=True, mainListConnection=sc)


class IdleCallbackData(object):
    function = None
    ID = None
    repeatCount = 'infinite'
    repeatInterval = 100

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


controlLinkAttr = 'link'


class nodeCacheData(object):
    """
    for caching the offset between an aux control and it's affected control
    """
    node = None
    isValid = False
    localMatrix = None
    worldMatrix = None

    def __init__(self, node_mob):
        self.node = node_mob
        self.cacheMatrix()

    def cacheMatrix(self):
        if not self.isValid:
            print 'self.node', self.node
            this_mfn_dep = om2.MFnDependencyNode(self.node)
            print 'this_mfn_dep', this_mfn_dep
            thisDagPath = om2.MDagPath.getAPathTo(self.node)
            print 'thisDagPath', thisDagPath

            controlPlug = this_mfn_dep.findPlug(controlLinkAttr, False)
            if not controlPlug:
                return
            if not controlPlug.isConnected:
                return

            controlNode = controlPlug.source().node()
            controlDagPath = om2.MDagPath.getAPathTo(controlNode)
            print 'control', controlDagPath
            control_mfn_dep = om2.MFnDependencyNode(controlNode)

            nodeMatrixPlug = this_mfn_dep.findPlug('worldMatrix', False).elementByLogicalIndex(0)
            nodeInverseMatrixPlug = this_mfn_dep.findPlug('parentInverseMatrix',
                                                          False).elementByLogicalIndex(0)
            controlMatrixPlug = control_mfn_dep.findPlug('worldMatrix', False).elementByLogicalIndex(0)

            nodeWorldMMatrix = om2.MFnMatrixData(nodeMatrixPlug.asMObject()).matrix()
            nodeParentInverseMMatrix = om2.MFnMatrixData(nodeInverseMatrixPlug.asMObject()).matrix()
            nodeWorldTransformMatrixObj = om2.MTransformationMatrix(nodeWorldMMatrix)
            nodeParentInverseTransformMatrixObj = om2.MTransformationMatrix(nodeParentInverseMMatrix)

            controlMMatrix = om2.MFnMatrixData(controlMatrixPlug.asMObject()).matrix()
            controlTransformMatrixObj = om2.MTransformationMatrix(controlMMatrix)

            resultMatrix = controlTransformMatrixObj.asMatrix() * nodeWorldTransformMatrixObj.asMatrix().inverse()

            self.localMatrix = resultMatrix
            self.worldMatrix = None
            self.isValid = True

            transformMatrixObj = om2.MTransformationMatrix(resultMatrix)
            translation = transformMatrixObj.translation(om2.MSpace.kWorld)
            rotation = transformMatrixObj.rotation(asQuaternion=False)
            print 'translation  : ', translation
            print 'rotation     : ', rotation
