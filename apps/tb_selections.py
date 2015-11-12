__author__ = 'tom.bailey'
import pymel.core as pm
import maya.cmds as cmds
import os, stat
import pickle
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
        self.main_set = self.create_main_set()
        self.save_dir = pm.optionVar.get('tb_qs_folder', 'c://qss//')
        self.qss_files = []
        pass

    def create_main_set(self):
        if not cmds.objExists("QuickSelects"):
            cmds.select(clear=True)
            main_set = cmds.sets(name="QuickSelects")
            cmds.select(self.selection, replace=True)
            return main_set
        else:
            return "QuickSelects"

    def create_qs_set(self):
        if self.selection:
            result = cmds.promptDialog(
            title='Quick selection name',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')

            if result == 'OK':
                qs_name = cmds.promptDialog(query=True, text=True)
                save = True
                if qs_name in self.all_sets:
                    if not cmds.confirmDialog(
                            title='Overwrite existing set?',
                            message='Are you sure?',
                            button=['Yes','No'],
                            defaultButton='Yes',
                            cancelButton='No',
                            dismissString='No'):
                        save = False
                if save:
                    self.save_qs(qs_name, self.selection)

        else:
            msg = "can't save a quick selection set with nothing selected!"
            message.error(position="botRight", prefix="Error", message=msg, fadeStayTime=3.0, fadeOutTime=4.0)

    def save_qs(self, qs_name, selection):
        print "saving ", qs_name, "with", selection
        pre_sel = cmds.ls(selection=True)
        # only select existing objects
        existing_obj = self.existing_obj_in_list(selection)
        if existing_obj:
            cmds.select(existing_obj, replace=True)

            if cmds.objExists(qs_name):
                if cmds.nodeType(qs_name) == 'objectSet':
                    cmds.delete(qs_name)
            qs = cmds.sets(name=qs_name, text="gCharacterSet")
            cmds.select(qs, replace=True)
            cmds.sets(qs,addElement=self.main_set)
            cmds.select(pre_sel, replace=True)

    def save_qs_to_file(self):
        self.all_sets = self.get_sets()
        result = cmds.promptDialog(
            title='Save quick select file',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
        if self.all_sets and result:
            file_name = cmds.promptDialog(query=True, text=True)
            save_file = os.path.join(self.save_dir,file_name+".qss")
            if not os.path.isdir(self.save_dir):
                print "making maya qss folder"
                os.mkdir(self.save_dir)
            else:
                os.chmod(self.save_dir, stat.S_IWRITE)
            out_data = []
            for qsets in self.all_sets:
                out_data.append(qss_data_obj(qs_name=str(qsets), qs_objects=self.get_set_contents(qsets)))
            pickle.dump( out_data, open(save_file, "wb" ) )

    def load_qss_file(self, qss_name):
        file_name = os.path.join(self.save_dir, qss_name)
        loaded_data = pickle.load(open(file_name, "rb"))
        for qs in loaded_data:
            self.save_qs(qs.qs_name, qs.qs_objects)

    def restore_qs_from_dir(self):
        for qss_files in os.listdir(self.save_dir):
            if qss_files.endswith(".qss"):
                self.qss_files.append(qss_files)
        if qss_files:
            self.restoreWin()

    def qss_widget(self, qss_name="", parent=""):
        rLayout = pm.rowLayout(numberOfColumns=2,
                               adjustableColumn=1,
                               columnWidth2=(200,50),
                               columnAttach2=("left", "right"),
                               parent=parent)
        pm.text(label=str(qss_name), parent=rLayout)

        pm.button(label="load", parent=rLayout, command=lambda *args : self.load_qss_file(qss_name))

    def restoreWin(self):
        if pm.window("qssLoader", exists=True):
            pm.deleteUI("qssLoader")
        qss_win = pm.window("qssLoader", width=300)
        layout = pm.columnLayout(adjustableColumn=True )
        pm.text(font="boldLabelFont",label="quick select files")

        scroll_layout = pm.scrollLayout(parent=layout, height=400)
        sub_layout = pm.columnLayout(adjustableColumn=True, parent=scroll_layout)

        for items in self.qss_files:
            print items
            self.qss_widget(qss_name=items, parent=sub_layout)

        pm.showWindow(qss_win)


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
    def existing_obj_in_list(sel):
        existing = []
        for ob in sel:
            if cmds.objExists(ob):
                existing.append(ob)
        return existing

    @staticmethod
    def get_set_contents(qss_set):
        return cmds.sets(qss_set, query=True )

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

class qss_data_obj():
    def __init__(self, qs_name="", qs_objects=[]):
        self.qs_name = qs_name
        self.qs_objects = qs_objects