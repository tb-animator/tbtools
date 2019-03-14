__author__ = 'Tom'
__author__ = 'tom.bailey'
import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm
import rig.spaceSwitch.tb_spaceSwitch as sw
reload(sw)


class cycler():
    def __init__(self):
        self.selection = pm.ls(selection=True)
        self.time_slider = mel.eval('$tmpVar=$gPlayBackSlider')
        self.hi_range = pm.timeControl(self.time_slider, query=True, rangeArray=True)
        self.time_range = self.get_range()
        self.current_frame = pm.getCurrentTime()
        self.length = self.time_range[1] - self.time_range[0]
        self.half_length = self.length * 0.5
        self.mid_point = self.time_range[0] + self.half_length
        self.fk_centre_attributes = ["rotateY", "rotateZ"]
        self.ik_attributes = ["translateX", "rotateY", "rotateZ", "AnimPivotX"]
        self.focalControl = self.getFocalControl(self.selection[0])
        print self.focalControl
        print self.time_range, "range"
        print self.mid_point, "mid point"

    def go(self):
        self.selection = pm.ls(selection=True)
        self.time_slider = mel.eval('$tmpVar=$gPlayBackSlider')
        self.hi_range = pm.timeControl(self.time_slider, query=True, rangeArray=True)
        self.time_range = self.get_range()
        self.current_frame = pm.getCurrentTime()
        self.length = self.time_range[1] - self.time_range[0]
        self.half_length = self.length * 0.5
        self.mid_point = self.time_range[0] + self.half_length
        self.fk_centre_attributes = ["rotateY", "rotateZ"]
        self.ik_attributes = ["translateX", "rotateY", "rotateZ", "AnimPivotX"]
        self.focalControl = self.getFocalControl(self.selection[0])
        print self.focalControl
        print self.time_range, "range"
        print self.mid_point, "mid point"

        if self.hi_range[0] == self.hi_range[1] - 1:
            print "not highlighted"
            self.process_range = [self.current_frame]
        else:
            self.process_range = [self.hi_range[0], self.hi_range[1] - 1]
            print "highlighted", self.process_range

        for num in range(int(self.process_range[0]), int(self.process_range[-1] + 1)):
            mirror_time = self.get_opposite_frame(num)
            print "current time", num, "mirror time", mirror_time
            for times in mirror_time:
                for obj in self.selection:
                    destination_obj = self.swap_left_right(obj)
                    if pm.keyframe(obj, query=True, time=num):
                        self.obj = obj
                        self.destination_obj = destination_obj[0]
                        self.mode = destination_obj[1]
                        self.time = num
                        self.destination_time = times
                        print "has key, lets mirror to ", destination_obj[0], "at time ", mirror_time, "mode is ", destination_obj[1]
                        self.mirror_attributes()
                    else :
                        print "no key on ", obj, "skipping"

    def getFocalControl(self, obj):
        namespace = obj.namespace()
        return "%s%s" % (namespace, "driver_root")

    def has_key(self, object, frame):
        return True

    def get_opposite_frame(self, frame):
        returnVal = []
        if frame == self.mid_point:
            returnVal = [self.time_range[0], self.time_range[1]]
        elif frame > self.mid_point and frame < self.time_range[1]:
            returnVal = [frame - self.half_length]
        elif frame == self.time_range[1]:
            returnVal = [self.mid_point]
        elif frame < self.mid_point and frame > self.time_range[0]:
            returnVal = [frame + self.half_length]
        elif frame == self.time_range[0]:
            returnVal = [self.mid_point]
        else:
            print "where???"
            returnVal = [frame]
        return returnVal

    def mirror_attributes(self):
        if self.mode == "fk":
            self.fk_copy()
        elif self.mode == "ik":
            self.ik_copy()

        elif self.mode == "fk_centre":
            self.fk_copy()
            self.flip_axis(self.fk_centre_attributes)
            print "mirror fk centre"
        elif self.mode == "ik_centre":
            self.fk_copy()
            self.flip_axis(self.ik_attributes)

    def ik_copy(self):
        pm.setCurrentTime(self.time)
        space = pm.getAttr(self.obj.attr('space'), time=self.time)
        destination_space = pm.getAttr(self.destination_obj.attr('space'), time=self.destination_time)
        # switch to driver root space
        _space_list = self.obj.space.getEnums()
        local_space = _space_list.value("driver_root")
        print "local space", local_space

        # put original object in local space
        sw.switch(self.obj, self.obj, int(local_space))

        # copy the current frame values
        pm.copyKey(self.obj, time=self.time)
        # change the time to mirror time
        pm.setCurrentTime(self.destination_time)
        # set destination object to local space
        sw.switch(self.destination_obj, self.destination_obj, int(local_space))
        # paste keys to destination
        pm.pasteKey(self.destination_obj, time=self.destination_time)
        # flip some curves
        self.flip_axis(self.ik_attributes)
        # put the space back again
        sw.switch(self.destination_obj, self.destination_obj, int(destination_space))
        # reset the spaces back to the original ones
        pm.setCurrentTime(self.time)
        print pm.getCurrentTime(), "this is the time fool"
        sw.switch(self.obj, self.obj, int(space))
        print "final space ", space


    def fk_copy(self):
        copied_keys = pm.copyKey(self.obj, time=self.time)
        pm.pasteKey(self.destination_obj, time=self.destination_time)
        print copied_keys

    def flip_axis(self, attributes):
        for attr in attributes:
            pm.setKeyframe(self.obj, time=self.time, insert=True, attribute=attr)
            in_angle = -1.0 * pm.keyTangent(self.obj, query=True, inAngle=True, time=self.time, attribute=attr)[0]
            out_angle = -1.0 * pm.keyTangent(self.obj, query=True, outAngle=True, time=self.time, attribute=attr)[0]

            flip_value = -1.0 * pm.keyframe(self.obj, query=True, time=self.time, valueChange=True, attribute=attr)[0]
            print self.obj, attr,  "in", in_angle, "out", out_angle, "v:", flip_value

            pm.setKeyframe(self.destination_obj, attribute=attr, value=flip_value, time=self.destination_time)
            pm.keyframe(self.destination_obj, attribute=attr, valueChange=flip_value, time=self.destination_time)
            print "hello ",attr , pm.keyframe(self.destination_obj, query=True, time=self.destination_time, valueChange=True, attribute=attr)[0]
            pm.keyTangent(self.destination_obj, edit=True, inAngle=in_angle, outAngle=out_angle,
                          time=self.destination_time, attribute=attr)

    def swap_left_right(self, obj):
        namespace = obj.namespace()
        name = obj.stripNamespace()
        mode = ""
        if name.startswith("l_"):
            name = name.replace("l_", "r_")
            mode = "ik"
        elif name.startswith("driver_l_"):
            name = name.replace("driver_l_", "driver_r_")
            mode = "fk"
        elif name.startswith("r_"):
            name = name.replace("r_", "l_")
            mode = "ik"
        elif name.startswith("driver_r_"):
            name = name.replace("driver_r_", "driver_l_")
            mode = "fk"
        elif name.startswith("driver_"):
            mode = "fk_centre"
        else:
            mode = "ik_centre"

        return [pm.PyNode("%s%s" % (namespace, name)), mode]

    def get_range(self):
        return [pm.playbackOptions(query=True, minTime=True), pm.playbackOptions(query=True, maxTime=True)]
