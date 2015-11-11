'''TB Animation Tools is a toolset for animators

*******************************************************************************
    License and Copyright
    Copyright 2015-Tom Bailey
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    send issues/ requests to brimblashman@gmail.com
    visit tb-animator.blogspot.com for "stuff"

    usage
    import tb_graphEditor as ge
    reload(ge)
    ge.graphEditor().open_graph_editor()
    # manually add selection callback
    ge.graphEditor().add_graph_editor_callback()

*******************************************************************************
'''

from tb_keyframe import keys
from tb_timeline import timeline
from tb_objectInfo import mod_panel
from tb_objectInfo import Attributes

import pymel.core as pm
import maya.mel as mel

# need to add this to an option window at some point
if not pm.optionVar(exists='tb_autoframe'):
    pm.optionVar(intValue=('tb_autoframe', 1))
if not pm.optionVar(exists='tb_graph_editor_callback'):
    pm.optionVar(intValue=('tb_graph_editor_callback', 1))

class graphEditor():
    def __init__(self):
        self.selection = pm.ls(selection=True)
        self.current_panel = mod_panel().getModelPanel()
        self.range = timeline.get_range()
        self.vertical_buffer = 0.2
        self.horizontal_buffer = 0.1
        self.selected_keys = sorted(keys.get_selected_keys())
        self.current_curves = keys.get_selected_curves()
        self.default_editor = 'graphEditor1GraphEd'
        self.graph_editors = pm.getPanel(scriptType="graphEditor")
        self.frame_range = []
        self.min_max = []
        self.select_connection = pm.animCurveEditor(
            self.default_editor,
            query=True,
            mlc=True
        )
        self.active_objects = pm.selectionConnection(
            self.select_connection,
            query=True,
            keyframeList=True,
            object=True
        )
        pass

    def smart_frame(self):
        if self.current_panel in self.graph_editors:
            self.smart_frame_graph_editor(shouldFilter=True)
        else:
            mel.eval("fitPanel -selected")

    def open_graph_editor(self):
        mel.eval('tearOffPanel "Graph Editor" "graphEditor" true;')
        self.smart_frame_graph_editor(shouldFilter=True)

    def smart_frame_graph_editor(self, mode='auto', shouldFilter=False):
        key_values = []
        if self.selected_keys and mode == 'auto':
            self.frame_range = [self.selected_keys[0], self.selected_keys[-1]]
            for curves in self.current_curves:
                key_values.extend(keys.get_key_values(curves))
        else:
            print "here"
            self.frame_range = [self.range[0], self.range[1]]
            active_objects = pm.selectionConnection(self.select_connection, query=True, keyframeList=True, object=True)
            print "active_objects", active_objects
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
        self.frame_range = self.get_buffer(self.frame_range, self.horizontal_buffer)
        if pm.animCurveEditor(self.default_editor, exists=True):
            pm.animView(self.default_editor,
                        startTime=self.frame_range[0],
                        endTime=self.frame_range[1]
                        )
            # if we got some min/max values then crop the vertical range as well
            if self.min_max:
                pm.animView(self.default_editor,
                            minValue=self.min_max[0],
                            maxValue=self.min_max[1]
                            )

        if shouldFilter:
            self.filter_graph_editor()


    def filter_graph_editor(self):
        self.remove_graph_editor_callback()
        self.current_curves = keys.get_selected_curves()
        channels = self.selection
        print "\nfilter section"
        print "channels", channels
        print "curves", self.current_curves
        current_connection = pm.selectionConnection('graphEditor1FromOutliner', query=True, object=True, keyframeList=True)
        animCurve_selection = pm.animCurveEditor(self.default_editor, query=True, mlc=True)
        active_objects = pm.selectionConnection(self.select_connection, query=True, keyframeList=True, object=True)
        print "active_objects", active_objects
        print "current_connection", current_connection
        print "animCurve_selection", animCurve_selection
        print "current_curves", self.current_curves

        if not self.current_curves:
            print "currently no curves selected so lets un filter everything"
            for channel in active_objects or channels:
                pm.selectionConnection('graphEditor1FromOutliner', edit=True, object=channel)
                # re frame new selection
                self.smart_frame_graph_editor()
        else:
            print "see this when filtering with selection only"
            for channel in current_connection:
                if channel not in self.current_curves:
                    print "deselecting ", channel
                    pm.selectionConnection('graphEditor1FromOutliner', edit=True, deselect=channel)

            for curves in self.current_curves:
                print "selecting", curves
                attr = Attributes().get_attribute_from_curve(curves)
                pm.selectionConnection('graphEditor1FromOutliner', edit=True, object=attr)

        self.add_graph_editor_callback()


    def add_graph_editor_callback(self):
        if pm.optionVar['tb_graph_editor_callback']:
            for graphEd in self.graph_editors:
                editor = str(graphEd) + "GraphEd"
                pm.selectionConnection(pm.animCurveEditor(editor,
                                                          query=True,
                                                          mlc=True),
                                       edit=True, addScript=graph_ed_callback)

    def remove_graph_editor_callback(self):
        for graphEd in self.graph_editors:
            editor = str(graphEd) + "GraphEd"
            pm.selectionConnection(pm.animCurveEditor(editor,
                                                      query=True,
                                                      mlc=True),
                                   edit=True, addScript="")

    @staticmethod
    def get_buffer(values, factor):
        offset = 0.0
        val_range = abs(values[0] - values[1])
        if abs(values[0] - values[1]) < 0.01:
            offset = 0.05
        min = values[0] - val_range * factor - offset
        max = values[1] + val_range * factor + offset
        return [min, max]


def graph_ed_callback(*args):
    if pm.optionVar['tb_autoframe']:
        graphEditor().smart_frame_graph_editor(mode='')
