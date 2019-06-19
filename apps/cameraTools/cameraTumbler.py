__author__ = 'tom.bailey'
import pymel.core as pm
import maya.cmds as cmds

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

def get_bounding_box_centre(objects):
    box = cmds.exactWorldBoundingBox(objects)  #Do standard BB computation
    x = ((box[0] + box[3]) / 2)
    y = ((box[1] + box[4]) / 2)
    z = ((box[2] + box[5]) / 2)
    return [x, y, z]

class tumbler():
    def __init__(self):
        print 'init'
        self.time = cmds.timerX()
        self.frequency = 0.1667
        if not pm.optionVar(exists='tumbler_enabled'):
            pm.optionVar(stringValue=('tumbler_enabled', 'enabled'))

    def toggle(self, state, *args):
        print args



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
            self.time = cmds.timerX() # set a new time stamp to prevent spamming

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
                    #print "skinning"
                    current_joint = cmds.artAttrSkinPaintCtx(current_context,
                                                             query=True,
                                                             influence=True)

            if current_joint:
                pivots.append(cmds.getAttr(current_joint +'.rotatePivot')[0])
            else:
                # selection
                for obj in selection:
                    object_type = cmds.nodeType(obj)
                    shape_node = cmds.listRelatives(obj, fullPath=True, shapes=True)
                    print "object:: ", object_type, shape_node

                    if shape_node:
                        print 'shape node'
                        shape_type = cmds.nodeType(shape_node[0])

                        if object_type == "transform":
                            if shape_type:
                                pivots.append(getPivot(obj))
                            else:
                                print 'no shape node'
                                pivots.append(cmds.getAttr(obj + '.rotatePivot')[0])
                        else:
                            pivots.append(getPivot(obj))
                    else:
                        if object_type == "joint":
                            # use rotate pivot of joints as they have no bounding box
                            pivots.append(getPivot(obj))
                            # print "joint!"
                        else:
                            pivots.append(getPivot(obj))
                            print "something else!"
            print pivots[0]
            self.update_tumble_pivots(midPoint(pivots))

def updateTumble(*args):
    global cTumbler
    cTumbler.doIt()
    '''
    try:
        cTumbler.doIt()
    except Exception as e:
        cTumbler = tumbler()
        cTumbler.doIt()
    '''