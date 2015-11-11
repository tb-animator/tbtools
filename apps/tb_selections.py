__author__ = 'tom.bailey'
import pymel.core as pm
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


class quick_selection():
    def __init__(self):
        pass