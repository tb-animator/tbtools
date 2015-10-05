__author__ = 'tom.bailey'
import maya.mel as mel
import pymel.core as pm
from tb_timeline import timeline

# nasty optionVar setup (sorry)
if not pm.optionVar(exists='op_play_view'):
    pm.optionVar(intValue=('op_play_view', 1))


def playBack(data):
    return playBackMod.DoIt(data)


class playBackMod(object):
    @classmethod
    def DoIt(cls, *args):
        """A function """
        pbm = cls()
        # lambda *args: checkBox_pressed(_name, args[0])

        if args:
            __dict = {"play": pbm.togglePlay,
                      "flip": pbm.togglePlay,
                      "crop": pbm.crop,
                      "shift_start": pbm.shift,
                      "shift_end": pbm.shift,
                      "crop_start": pbm.crop,
                      "crop_end": pbm.crop
                      }
            _message = __dict[args[0]](args)

        else:
            _message = pbm.togglePlay()
        if _message:
            pm.inViewMessage(amg=_message,
                          pos='botLeft',
                          fadeStayTime=len(_message)+500.0,
                          fadeOutTime=300.0,
                          fade=True)

        return pbm

    def __init__(self):
        self.time_slider = mel.eval('$tmpVar=$gPlayBackSlider')
        self.hi_range = pm.timeControl(self.time_slider, query=True, rangeArray=True)
        self.play_state = pm.play(query=True, state=True)
        self.time_range = [pm.optionVar['pb_start'], pm.optionVar['pb_end']]

    def crop(self, *args):
        if args[0][0] == "crop" or not self.hi_range[0] == self.hi_range[1]-1:
            self.crop_range()
            _message = 'cropping timeline from <hl>%s</hl> to <hl>%s</hl> ' % (self.hi_range[0],self.hi_range[1])
        else:
            _time = pm.getCurrentTime()
            if args[0][0] == "crop_start":
                pm.playbackOptions(minTime=_time)
                _message = 'cropping timeline from <hl>%s</hl>' % _time
            else:
                pm.playbackOptions(maxTime=_time)
                _message = 'cropping timeline to <hl>%s</hl>' % _time
        return _message

    def shift(self, *args):
        _time = pm.getCurrentTime()
        _range = timeline().get_range()[1]-timeline().get_range()[0]
        _new_range = [0, 0]
        if "shift_start" == args[0][0]:
            _new_range = [_time, _time+_range]
        else:
            _new_range = [_time-_range, _time]
        _message = 'shifting timeline from <hl>%s:%s</hl> to <hl>%s:%s</hl>' % (timeline().get_range()[0],
                                                                                timeline().get_range()[1],
                                                                                _new_range[0],
                                                                                _new_range[1])
        pm.playbackOptions(minTime=_new_range[0], maxTime=_new_range[1])
        return _message

    def togglePlay(self, args):
        _message = ''
        _flip_message = ["","\nPlaying every frame"]
        if not self.play_state:
            self.cache_range()
            _flipping = args[0] == "flip"
            pm.playbackOptions(maxPlaybackSpeed=not _flipping)

            # not playing so start now
            if not self.hi_range[0] == self.hi_range[1]-1:

                # range highlighted
                self.crop_range()
                pm.setCurrentTime(self.hi_range[0])
                _message = 'playing timeline segment <hl>%s</hl> to <hl>%s</hl> %s' % (self.hi_range[0],
                                                                                       self.hi_range[1],
                                                                                       _flip_message[_flipping])
            else:
                _message = 'playing'
        else:
            if timeline().get_range()[0] != self.time_range[0]:
                _message = 'reverting timeline to <hl>%s:%s</hl> ' % (self.time_range[0], self.time_range[1])
            # stopping playback and reset crop
            else:
                _message = 'pausing'
            self.reset_range()

        pm.play(state=not self.play_state)
        NT_CameraTumbler.tumbler().doIt()
        if pm.optionVar['op_play_view']:
            return _message
        else:
            return ''


    def cache_range(self):
        self.time_range = timeline().get_range()

        pm.optionVar(floatValue=('pb_start', self.time_range[0]))
        pm.optionVar(floatValue=('pb_end', self.time_range[1]))

    def crop_range(self):
        pm.playbackOptions(minTime=self.hi_range[0],
                           maxTime=self.hi_range[1])

    def reset_range(self):

        pm.playbackOptions(minTime=self.time_range[0],
                           maxTime=self.time_range[1])


def __init_option__():
    # should only happen once
    if not pm.optionVar(exists='pb_start'):
        pm.optionVar(floatValue=('pb_start', pm.playbackOptions(q=True, minTime=True)))
    if not pm.optionVar(exists='pb_end'):
        pm.optionVar(floatValue=('pb_end', pm.playbackOptions(q=True, maxTime=True)))

# check if we don't the option vars set up yet
if not pm.optionVar(exists='pb_start'):
    __init_option__()
