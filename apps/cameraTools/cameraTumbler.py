__author__ = 'tom.bailey'
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
from tb_decorators import decorator
from tb_units import unit_conversion

# does it come in black?

global cTumbler


def midPoint(pointArray):
    midPoint = [0, 0, 0]

    # Get Center Point
    total = len(pointArray)
    for point in pointArray:
        midPoint = [midPoint[0] + point[0], midPoint[1] + point[1], midPoint[2] + point[2]]

    # Calculate Average Position
    midPoint = [midPoint[0] / total, midPoint[1] / total, midPoint[2] / total]

    # Return Result
    return midPoint


def getPivot(obj):
    return cmds.xform(obj, query=True, rotatePivot=True, worldSpace=True)

def getPivotAsBbox(boundingBox, obj):
    pivot = cmds.xform(obj, query=True, rotatePivot=True, worldSpace=True)
    if not boundingBox:
        return [pivot[0], pivot[1], pivot[2], pivot[0], pivot[1], pivot[2]]
    else:
        lowX = min(pivot[0], boundingBox[0])
        lowY = min(pivot[1], boundingBox[1])
        lowZ = min(pivot[2], boundingBox[2])
        highX = max(pivot[0], boundingBox[3])
        highY = max(pivot[1], boundingBox[4])
        highZ = max(pivot[2], boundingBox[5])
        return [lowX, lowY, lowZ, highX, highY, highZ]

def get_bbox(boundingBox, obj):
    bbox = cmds.exactWorldBoundingBox(obj)
    if not boundingBox:
        return bbox
    else:
        lowX = min(bbox[0], boundingBox[0])
        lowY = min(bbox[1], boundingBox[1])
        lowZ = min(bbox[2], boundingBox[2])
        highX = max(bbox[3], boundingBox[3])
        highY = max(bbox[4], boundingBox[4])
        highZ = max(bbox[5], boundingBox[5])
        return [lowX, lowY, lowZ, highX, highY, highZ]

def get_bounding_box_mid(box):
    x = ((box[0] + box[3]) / 2)
    y = ((box[1] + box[4]) / 2)
    z = ((box[2] + box[5]) / 2)
    return [x, y, z]

def get_bounding_box_centre(objects):
    box = cmds.exactWorldBoundingBox(objects)  # Do standard BB computation
    x = ((box[0] + box[3]) / 2)
    y = ((box[1] + box[4]) / 2)
    z = ((box[2] + box[5]) / 2)
    return [x, y, z]


def getMoveManipPosition(*args):
    return cmds.manipMoveContext('Move', query=True, position=True)


def getRotateManipPosition(*args):
    return cmds.manipRotateContext('Rotate', query=True, position=True)


def getScaleManipPosition(*args):
    return cmds.manipScaleContext('Scale', query=True, position=True)


def getSelectManipPosition(*args):
    # hack to set manipulator pivot when in component selection mode
    mel.eval("setToolTo $gMove;")
    pos = cmds.manipMoveContext('Move', query=True, position=True)
    mel.eval("setToolTo $gSelect")
    return pos


class tumbler():
    def __init__(self):
        print 'init'
        self.time = cmds.timerX()
        self.frequency = 0.1667
        self.contextQuery = {'manipMove': getMoveManipPosition,
                             'manipRotate': getRotateManipPosition,
                             'manipScale': getScaleManipPosition,
                             'selectTool': getSelectManipPosition}

        if not pm.optionVar(exists='tumbler_enabled'):
            pm.optionVar(stringValue=('tumbler_enabled', 'enabled'))

    def reset_tumble(self, *args):
        pivot = [0, 0, 0]
        self.update_tumble_pivots(pivot)
        all_cameras = cmds.ls(dag=True, cameras=True)
        for cam in all_cameras:
            try:
                # set the tumble pivot of the camera to the coordinates we have calculated before
                cmds.setAttr(cam + ".tumblePivot", pivot[0], pivot[1], pivot[2])
            except Exception as e:
                print e.message

    def update_tumble_pivots(self, pivot):
        # Do the actual tumble pivot setting
        all_cameras = cmds.ls(dag=True, cameras=True)
        cmds.tumbleCtx("tumbleContext", edit=True,
                       localTumble=0)  # Set the tumble tool to honor the cameras tumble pivot
        pivot[0] *= unit_conversion()
        pivot[1] *= unit_conversion()
        pivot[2] *= unit_conversion()
        for cam in all_cameras:
            try:
                # set the tumble pivot of the camera to the coordinates we have calculated before
                cmds.setAttr(cam + ".tumblePivot", pivot[0], pivot[1], pivot[2])
            except:
                Warning("Setting camera tumble pivot on " + cam + "failed!")

    def elapsedTime(self):
        # print 'last call', self.time + self.frequency, 'current time', cmds.timerX()
        return self.time + self.frequency < cmds.timerX()

    @decorator.undoToggle
    def doIt(self, *args):
        if pm.optionVar['tumble_enabled'] == 'enabled' and self.elapsedTime():
            self.time = cmds.timerX()  # set a new time stamp to prevent spamming

            selection = cmds.ls(selection=True)
            if not selection:
                return None
            pivots = []
            current_context = cmds.currentCtx()
            current_tool = ""
            if cmds.contextInfo(current_context, exists=True):
                current_tool = cmds.contextInfo(current_context, c=True)
            current_joint = ""
            print "current_tool", current_tool, "current_context", current_context
            if current_tool == "artAttrSkin":
                whichTool = cmds.artAttrSkinPaintCtx(current_context, query=True, whichTool=True)
                if whichTool == "skinWeights":
                    current_joint = cmds.artAttrSkinPaintCtx(current_context,
                                                             query=True,
                                                             influence=True)
                if len(selection) > 1:
                    mel.eval("setToolTo $gMove;")
                    self.update_tumble_pivots(cmds.manipMoveContext('Move', query=True, position=True))
                    mel.eval("ArtPaintSkinWeightsToolOptions")
                    return
                elif current_joint:
                    print current_joint
                    self.update_tumble_pivots(cmds.xform(current_joint,
                                             query=True,
                                             worldSpace=True,
                                             absolute=True,
                                             translation=True))
                    return
            else:
                boundingBox = []
                selected_objects = cmds.ls(transforms=True, selection=True)
                selected_shapes = cmds.ls(selection=True, shapes=True)
                non_component_selection = []
                non_component_selection.extend(selected_shapes)
                non_component_selection.extend(selected_objects)
                selected_components = [x for x in cmds.ls(selection=True) if x not in non_component_selection]
                # if there's a component selection like vertex/face use the manipulator position for the pivot
                if selected_components:
                    pivots.append(self.contextQuery[cmds.contextInfo(cmds.currentCtx(), c=True)]())
                # selection
                else:
                    if selected_objects:
                        transforms_with_shapes = [x for x in selected_objects if cmds.listRelatives(x, fullPath=True, shapes=True)]
                        transforms_without_shapes = [x for x in selected_objects if x not in transforms_with_shapes]
                        if transforms_with_shapes:
                            self.boundingBox = get_bbox(None, transforms_with_shapes)
                        if transforms_without_shapes:
                            for x in transforms_without_shapes:
                                self.boundingBox = getPivotAsBbox(boundingBox, x)
                    if boundingBox:
                        self.update_tumble_pivots(get_bounding_box_mid(self.boundingBox))

            if pivots:
                print 'pivots ooo', pivots
                self.update_tumble_pivots(midPoint(pivots))


def updateTumble(*args):
    global cTumbler

    try:
        cTumbler.doIt()
    except Exception as e:
        cTumbler = tumbler()
        cTumbler.doIt()
