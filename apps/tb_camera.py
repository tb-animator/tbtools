__author__ = 'tom.bailey'
import pymel.core as pm

from tb_decorators import decorator
from tb_units import unit_conversion

# does it come in black?

global cTumbler

class tumbler():
    def __init__(self):
        print 'init'
        self.time = pm.timerX()
        self.frequency = 0.1667
        if not pm.optionVar(exists='tumble_enabled'):
            pm.optionVar(stringValue=('tumble_enabled', 0))
        ver = pm.about(version=True)
        '''
        if ver == '2016':
            self.units = self.get_units(pm.currentUnit(query=True, linear=True))
        else:
            self.units = 100.0
        pass
        '''

    def toggle(self, state, *args):
        print args

    def get_bounding_box_centre(self, objects):
        box = pm.exactWorldBoundingBox(objects)  #Do standard BB computation
        x = ((box[0] + box[3]) / 2)
        y = ((box[1] + box[4]) / 2)
        z = ((box[2] + box[5]) / 2)
        return [x, y, z]

    def reset_tumble(self, *args):
        pivot = [0, 0, 0]
        self.update_tumble_pivots(pivot)
        all_cameras = pm.ls(dag=True, cameras=True)
        for cam in all_cameras:
            try:
                # set the tumble pivot of the camera to the coordinates we have calculated before
                pm.setAttr(cam + ".tumblePivot", pivot[0], pivot[1], pivot[2])
            except Exception as e:
                print e.message

    def update_tumble_pivots(self, pivot):
        # Do the actual tumble pivot setting
        all_cameras = pm.ls(dag=True, cameras=True)
        pm.tumbleCtx("tumbleContext", edit=True,
                     localTumble=0)  # Set the tumble tool to honor the cameras tumble pivot
        pivot[0] *= unit_conversion()
        pivot[1] *= unit_conversion()
        pivot[2] *= unit_conversion()
        for cam in all_cameras:
            try:
                # set the tumble pivot of the camera to the coordinates we have calculated before
                pm.setAttr(cam + ".tumblePivot", pivot[0], pivot[1], pivot[2])
            except:
                Warning("Ritalin: Setting camera tumble pivot on " + cam + "failed!")

    def elapsedTime(self):
        # print 'last call', self.time + self.frequency, 'current time', pm.timerX()
        return self.time + self.frequency < pm.timerX()

    @decorator.undoToggle
    def doIt(self, *args):

        if pm.optionVar['tumble_enabled'] and self.elapsedTime():
            self.time = pm.timerX() # set a new time stamp to prevent spamming

            selection = pm.ls(selection=True)
            bounding_boxes = []
            current_context = pm.currentCtx()
            current_tool = ""
            if pm.contextInfo(current_context, exists=True):
                current_tool = pm.contextInfo(current_context, c=True)
            current_joint = ""
            # print "current_tool", current_tool, "current_context", current_context
            if current_tool == "artAttrSkin":
                whichTool = pm.artAttrSkinPaintCtx(current_context, query=True, whichTool=True)
                if whichTool == "skinWeights":
                    #print "skinning"
                    current_joint = pm.PyNode(pm.artAttrSkinPaintCtx(
                        current_context,
                        query=True,
                        influence=True))

            # only work when you have a seleciton
            if len(selection) > 0:
                if current_joint:
                    bounding_boxes.append(current_joint.rotatePivot)
                else:
                    # selection
                    for obj in selection:
                        object_type = pm.nodeType(obj)
                        shape_node = pm.listRelatives(obj, fullPath=True, shapes=True)
                        # print "object:: ", object_type, shape_node

                        if shape_node:
                            shape_type = pm.nodeType(shape_node[0])

                            if object_type == "transform":
                                if shape_type:
                                    #bounding_boxes.append(obj)
                                    bounding_boxes.append(obj.rotatePivot)
                                    # print shape_type, "bounding box"
                                else:
                                    bounding_boxes.append(obj.rotatePivot)
                            else:
                                bounding_boxes.append(obj)
                        else:
                            if object_type == "joint":
                                # use rotate pivot of joints as they have no bounding box
                                bounding_boxes.append(obj.rotatePivot)
                                # print "joint!"
                            else:
                                bounding_boxes.append(obj)
                                # print "something else!"

                # get the centre of the box
                pivot_centre = self.get_bounding_box_centre(bounding_boxes)

                self.update_tumble_pivots(pivot_centre)
            # pm.undoInfo(stateWithoutFlush=True)

            '''if len(selection) == 0:
                pivot = [0, 0, 0]
                self.update_tumble_pivots(pivot)'''


def updateTumble(*args):
    global cTumbler
    try:
        cTumbler.doIt()
    except Exception as e:
        cTumbler = tumbler()
        cTumbler.doIt()