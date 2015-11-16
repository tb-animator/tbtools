__author__ = 'Tom'
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


*******************************************************************************
'''
import tb_timeline as tl
import pymel.core as pm

class playback():
    def __init__(self):
        self.playback_state = pm.play(query=True, state=True)
        self.timeline = tl.timeline()
        print self.timeline.info()

    def get_flip_frames(self):
        return pm.optionVar.get('tb_flip_frames', 10)

    def isPlaying(self):
        return pm.play(query=True, state=True)

    def playPause(self, flip=False):
        # currently playing, so reset any time range
        print "play state", self.isPlaying()
        if self.isPlaying():
            if self.timeline.cached_range:
                self.timeline.set_min(time=self.timeline.cached_range[0])
                self.timeline.set_max(time=self.timeline.cached_range[1])
            pm.playbackOptions(query=True,playbackSpeed=1)
        # not currently playing
        else:
            # store the current playback range
            self.timeline.cached_range = self.timeline.cache_range()
            # not playing, crop the timeline if there is a highlighted selection
            if self.timeline.isHighlighted():
                print "should crop before playing"

                pm.setCurrentTime(self.timeline.get_highlighted_range(min=True))
                self.timeline.set_min(time=self.timeline.get_highlighted_range(min=True))
                self.timeline.set_max(time=self.timeline.get_highlighted_range(max=True))
            elif flip:
                pm.setCurrentTime(self.timeline.get_highlighted_range(min=True))
                self.timeline.set_min(time=self.timeline.get_highlighted_range(min=True))
                self.timeline.set_max(time=self.timeline.get_highlighted_range(min=True)+self.get_flip_frames())


        pm.play(state=not self.isPlaying())
