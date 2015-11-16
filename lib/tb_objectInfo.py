__author__ = 'tom.bailey'
import pymel.core as pm


# this class should handle getting the relevant model panel with focus or under pointer
# failing that it will get the first valid model panel it can find

class mod_panel():
    def __init__(self):
        pass

    # get the current model panel
    def getModelPanel(self):
        curPanel = pm.getPanel(underPointer=True) or pm.getPanel(withFocus=True)
        if pm.objectTypeUI(curPanel) == 'modelEditor':
            return curPanel
        else:
            return self.get_modelEditors(pm.lsUI(editors=True))[0]

    @staticmethod
    def filter_modelEditors(editors):
        return pm.objectTypeUI(editors) == 'modelEditor'

    def get_modelEditors(self, editors):
        return filter(self.filter_modelEditors, editors)


# used for weird lookups for graph editor curve framing
class Attributes():
    def __init__(self):
        pass

    @staticmethod
    def get_attribute_from_curve(debug=False, curve=""):
        attr = None
        char_node = pm.listConnections(curve, type='character', destination=True)
        if char_node:
            conns = pm.listConnections(curve, destination=True, plugs=True)
            print conns
            attr = pm.listConnections(conns, destination=True, source=False, plugs=True)[0]
        else:
            attr = pm.listConnections(curve, destination=True, plugs=True)[0]
        if debug:
            print "attr ", attr, " found for curve", curve
        return attr