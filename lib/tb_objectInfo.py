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