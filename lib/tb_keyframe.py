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

    this script holds a bunch of useful keyframe related functions to make life easier

    send issues/ requests to brimblashman@gmail.com
    visit tb-animator.blogspot.com for "stuff"

*******************************************************************************
'''

import pymel.core as pm
import maya.cmds as mc

class keys():
    def __init__(self):
        pass

    def get(self):
        pass

    @staticmethod
    def get_selected_curves():
        """ returns the currently selected curve names
        """
        return pm.keyframe(query=True, selected=True, name=True)

    @staticmethod
    def get_selected_keys():
        """ returns the currently selected curve names
        """
        return pm.keyframe(query=True, selected=True)

    @staticmethod
    def get_selected_keycount():
        return pm.keyframe(selected=True, query=True, keyframeCount=True)

    @staticmethod
    def get_key_times(curve):
        return pm.keyframe(curve, query=True, selected=True, timeChange=True)

    @staticmethod
    def get_key_values(curve):
        return pm.keyframe(curve, query=True, selected=True, valueChange=True)

    @staticmethod
    def get_key_values_from_range(curve, time_range):
        return pm.keyframe(curve, query=True, time=time_range, valueChange=True)


class key_mod():

    def __init__(self):
        pass

    def match(self, data):
        ## match tangents for looping animations
        #
        # from tb_keyframe import key_mod
        # key_mod().match("start")
        # or
        # key_mod().match("end")
        #
        __dict = {'start': True, 'end': False
                  }
        state = __dict[data]
        print "state", state
        print "mode", data
        s = mc.playbackOptions(query=True, min=state, max=not state)
        e = mc.playbackOptions(query=True, max=state, min=not state)
        animcurves = mc.keyframe(query=True, name=True)
        tangent = []
        if animcurves and len(animcurves):
            for curve in animcurves:
                tangent = [mc.keyTangent(curve, query=True, time=(s, s), outAngle=state, inAngle=not state)[0],
                           mc.keyTangent(curve, query=True, time=(e, e), outAngle=state, inAngle=not state)[0]]
                mc.keyTangent(curve, edit=True, lock=False, time=(e, e),
                              outAngle=tangent[state], inAngle=tangent[not state])
        else:
            print "no anim curves found"