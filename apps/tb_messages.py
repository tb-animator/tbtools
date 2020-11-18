__author__ = 'Tom.Bailey'

import pymel.core as pm


class Message():
    def __init__(self):
        self.positions = ["topLeft",
                          "topCenter",
                          "topRight",
                          "midLeft",
                          "midCenter",
                          "midCenterTop",
                          "midCenterBot",
                          "midRight",
                          "botLeft",
                          "botCenter",
                          "botRight"]
        self.optionVar_name = "inViewMessageEnable"
        self.inView_opt = pm.optionVar.get("inViewMessageEnable")
        self.colours = {'green': 'style=\"color:#33CC33;\"',
                        'red': 'style=\"color:#FF0000;\"',
                        'yellow': 'style=\"color:#FFFF00;\"',
                        }

    # this disables the default maya inview messages (which are pointless after a while)
    def disable_messages(self):
        pm.optionVar(intValue=(Message().optionVar_name, 0))
        pass

    def enable_messages(self):
        pm.optionVar(intValue=(Message().optionVar_name, 1))
        pass


# yellow info prefix highlighting
class info(Message):
    def __init__(self, position="midCenter", prefix="", message="", fadeStayTime=2.0, fadeOutTime=2.0, fade=True):
        prefix = '<hl>%s</hl>' % prefix
        Message().enable_messages()
        pm.inViewMessage(amg=prefix + message,
                         pos=position,
                         fadeStayTime=fadeStayTime,
                         fadeOutTime=fadeOutTime,
                         fade=fade)
        Message().disable_messages()


# prefix will be highlighted in red!
class error(Message):
    def __init__(self, position="midCenter", prefix="", message="", fadeStayTime=0.5, fadeOutTime=4.0, fade=True):
        #self.optionVar_name = "inViewMessageEnable"
        # self.optionVar_name = Message().optionVar_name
        prefix = '<span %s>%s</span>' % (Message().colours['red'], prefix)
        Message().enable_messages()
        pm.inViewMessage(amg='%s : %s' % (prefix, message),
                         pos=position,
                         fadeOutTime=fadeOutTime,
                         dragKill=True,
                         fade=fade)
        Message().disable_messages()