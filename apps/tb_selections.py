__author__ = 'tom.bailey'
import pymel.core as pm
import maya.cmds as cmds
import tb_messages as message

# selects all nodes in a character set
def select_cheracter_set():
    selection = pm.ls(selection=True)
    _characters = []  # will be a list of all associated character sets to seleciton
    if selection:
        for obj in selection:
            _char = pm.listConnections(obj, destination=True,
                                       connections=True,
                                       type='character')
            if _char:
                if not _char[0][1] in _characters:
                    _characters.append(_char[0][1])

        out_obj = []
        for char in _characters:
            _obj_list = pm.sets(char, query=True, nodesOnly=True)
            for obj in _obj_list:
                out_obj.append(obj)
        pm.select(out_obj, add=True)
    else:
        msg = 'no character sets found for selection'
        message.error(position="botRight", prefix="Error", message=msg, fadeStayTime=3.0, fadeOutTime=4.0)


# this will find quick selection sets, and if you currently have one object in a set selected
# it will select the whole set

class quick_selection():
    def __init__(self):
        self.all_sets = self.get_sets()
        self.selection = cmds.ls(selection=True)
        pass

    def create_qs_set(self):
        pass

    def save_qs_to_file(self):
        pass

    def restore_qs_from_file(self):
        pass

    def qs_select(self):
        if self.selection:
            if self.all_sets:
                for a_set in self.all_sets:
                    qs_result = self.check_set_membership(self.selection, a_set)
                    if qs_result:
                        cmds.select(a_set, add=True)
            else:
                msg = 'no quick selects found for selection'
                message.error(position="botRight", prefix="Error", message=msg, fadeStayTime=3.0, fadeOutTime=4.0)


    @staticmethod
    def get_sets():
        all_sets = cmds.ls(sets=True)
        qs_sets = []
        for a_set in all_sets:
            if cmds.sets(a_set, query=True, text=True) == 'gCharacterSet':
                qs_sets.append(a_set)
        return qs_sets

    @staticmethod
    def check_set_membership(selection, sel_set):
        sel_set_members = cmds.sets(sel_set, query=True)
        if [ i for i in selection if i in sel_set_members]:
            return sel_set
        else:
            return None