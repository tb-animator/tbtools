__author__ = 'tom.bailey'

from tb_keyframe import keys
from lib.tb_timeline import timeline
import pymel.core as pm


class graphEditor():
    def __init__(self):
        self.selection = pm.ls(selection=True)
        self.range = timeline.get_range()
        self.vertical_buffer = 0.2
        self.selected_keys = sorted(keys.get_selected_keys())
        self.current_curves = keys.get_selected_curves()
        self.default_editor = 'graphEditor1GraphEd'
        self.frame_range = []
        self.min_max = []
        self.select_connection = pm.animCurveEditor(self.default_editor, query=True, mlc=True)
        pass

    def smart_frame(self):
        print self.range
        print self.selected_keys
        print self.current_curves
        key_values = []
        if self.selected_keys:
            self.frame_range = [self.selected_keys[0], self.selected_keys[-1]]
            for curves in self.current_curves:
                key_values.extend(keys.get_key_values(curves))

        else:
            self.frame_range = [self.range[0], self.range[1]]
            active_objects = pm.selectionConnection(self.select_connection, query=True, keyframeList=True, object=True)
            print active_objects
            if active_objects:
                for obj in active_objects:
                    try:
                        key_values.extend(keys.get_key_values_from_range(obj, self.range))
                    except:
                        pass

        # sort the key values to get the range
        if key_values:
            self.min_max = sorted(key_values)
            self.min_max = self.get_buffer([self.min_max[0], self.min_max[-1]], self.vertical_buffer)

        # crop the timeline range
        if pm.animCurveEditor(self.default_editor, exists=True):
            pm.animView(self.default_editor,
                        startTime=self.frame_range[0]-5,
                        endTime=self.frame_range[1]+5
                        )
            # if we got some min/max values then crop the vertical range as well
            if self.min_max:
                pm.animView(self.default_editor,
                            minValue=self.min_max[0],
                            maxValue=self.min_max[1]
                            )
        # fitPanel -selected

    @staticmethod
    def get_buffer(values, factor):
        offset = 0.0
        if abs(values[0]-values[1]) < 0.01:
            offset = 0.05
        min = values[0] - abs(values[0]*factor) - offset
        max = values[1] + abs(values[1]*factor) + offset
        print values, min, max
        return [min, max]