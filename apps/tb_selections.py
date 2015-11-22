__author__ = 'tom.bailey'
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
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


# class for pickwalking, supports message attributes (more reliable)
class pickwalker():
    def __init__(self):
        self.up = 'cgTkPickWalkup'
        self.down = 'cgTkPickWalkdown'
        self.left = 'cgTkPickWalkleft'
        self.right = 'cgTkPickWalkright'

    def walk(self, up=False, down=False, left=False, right=False, add=False):
        if up:
            dir = self.up
            cmd = "pickWalkUp"
        elif down:
            dir = self.down
            cmd = "pickWalkDown"
        elif left:
            dir = self.left
            cmd = "pickWalkLeft"
        elif right:
            dir = self.right
            cmd = "pickWalkRight"

        allObj = pm.ls(selection=True)
        if allObj:
            return_objs = []
            for obj in allObj:
                try:
                    attribute = pm.Attribute(obj + "." + dir)
                    print attribute
                    print attribute, attribute.exists(), attribute.type()
                    if attribute.exists():
                        # check if the attribute is a message attr
                        if attribute.type() == 'message':
                            destination = pm.listConnections(attribute)
                            return_objs.append(destination)
                        else:
                            # get string attr
                            destination = pm.PyNode("%s%s" % (obj.namespace(), attribute.get() ))
                            return_objs.append(destination)
                except:
                    pass
            if return_objs:
                pm.select(return_objs, replace=not add, add=add)
            else:
                mel.eval(cmd)
                if add:
                    pm.select(allObj, add=True)

# this will find quick selection sets, and if you currently have one object in a set selected
# it will select the whole set

class quick_selection():
    def __init__(self):
        self.all_sets = self.get_sets()
        self.selection = cmds.ls(selection=True)
        self.main_set = self.create_main_set()
        self.save_dir = pm.optionVar.get('tb_qs_folder', 'c://qss//')
        self.qss_files = []
        self.rb_col = None
        self.ns_text = None
        self.namespace_mode = ""

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
        # make sure we have the main set

        # only select existing objects
        existing_obj = self.existing_obj_in_list(selection)
        if existing_obj:
            cmds.select(existing_obj, replace=True)

            if cmds.objExists(qs_name):
                if cmds.nodeType(qs_name) == 'objectSet':
                    cmds.delete(qs_name)
            self.create_main_set()
            qs = cmds.sets(name=qs_name, text="gCharacterSet")
            cmds.select(qs, replace=True)
            cmds.sets(qs,addElement=self.main_set)
            cmds.select(pre_sel, replace=True)
        self.create_main_set()

    # get data loaded from a qss file but muck about with namespaces first
    def save_qs_from_file(self, qs_name, selection):
        def process_namespace():
            sel = pm.ls(selection=True)
            if sel:
                namespace_override = sel[0].namespace()
                print namespace_override
            else:
                print "no selection!"
            if namespace_override:
                print "namespace overridden" , namespace_override
            else:
                print "no namespace on sel"
            for sel in selection:
                processed_list.append(namespace_override + sel.split(":")[-1])
            return processed_list

        def replace_namespace(namespace=""):
            for sel in selection:
                processed_list.append(namespace + sel.split(":")[-1])

        print self.namespace_mode
        print selection
        processed_list = []
        if self.namespace_mode == "sel":
            processed_list = process_namespace()
            msg = 'quick selects created for %s' % qs_name
        elif self.namespace_mode == "spec":
            processed_list = replace_namespace(namespace=pm.textField(self.ns_text, query=True, text=True))
            msg = 'no quick selects created for specified namespace %s' % qs_name
        else:
            processed_list = selection
            msg = 'quick selects created for %s' % qs_name
        print processed_list
        if processed_list:
            self.save_qs(qs_name, processed_list)
            message.info(position="botRight", prefix="info", message=msg, fadeStayTime=5, fadeOutTime=5.0)
        else:
            # process failed, make error
            message.error(position="botRight", prefix="Error", message=msg, fadeStayTime=5, fadeOutTime=5.0)

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
            self.save_qs_from_file(qs.qs_name, qs.qs_objects)

    # gets the list of qss files
    def restore_qs_from_dir(self):
        for qss_files in os.listdir(self.save_dir):
            if qss_files.endswith(".qss"):
                self.qss_files.append(qss_files)
        if qss_files:
            self.restoreWin()

    # mini ui with a button!
    def qss_widget(self, qss_name="", parent=""):
        rLayout = pm.rowLayout(numberOfColumns=2,
                               adjustableColumn=1,
                               columnWidth2=(180,50),
                               columnAttach2=("left", "right"),
                               parent=parent)
        pm.text(label=str(qss_name), parent=rLayout)

        pm.button(label="load", parent=rLayout, command=lambda *args : self.load_qss_file(qss_name))

    def get_ns_mode(self):
        print self.namespace_mode


    def namespace_widget(self, parent=""):
        def fileMode(*args):
            self.namespace_mode = "file"
        def selMode(*args):
            self.namespace_mode = "sel"
        def specMode(*args):
            self.namespace_mode = "spec"

        fLayout = pm.frameLayout(parent=parent, label="please select namespace source")
        cLayout = pm.columnLayout()
        r_layout = pm.rowLayout(numberOfColumns=2,
                                columnWidth1=60,
                                adjustableColumn=2)
        pm.columnLayout(width = 150)
        pm.text(label="namespace source")
        pm.text(label="")
        pm.setParent(r_layout)
        g_layout = pm.gridLayout(numberOfColumns=2, cellWidthHeight=(100,20))
        self.rb_col = pm.radioCollection()
        print self.rb_col
        rb_file = pm.radioButton(collection=self.rb_col,
                                 label='from file',
                                 onCommand=fileMode)
        rb_sel = pm.radioButton("fromSel",
                                collection=self.rb_col,
                                label='from selection',
                                onCommand=selMode)
        rb_spec = pm.radioButton("spec",
                                 collection=self.rb_col,
                                 label='specify',
                                 onCommand=specMode)
        pm.radioCollection( self.rb_col, edit=True, select=rb_file )
        self.ns_text = pm.textField()


    # ui for loading sets
    def restoreWin(self):
        if pm.window("qssLoader", exists=True):
            pm.deleteUI("qssLoader")
        qss_win = pm.window("qssLoader", width=300, height=400)
        layout = pm.columnLayout(adjustableColumn=True )
        pm.text(font="boldLabelFont",label="quick select files")

        scroll_layout = pm.scrollLayout(parent=layout,
                                        childResizable=True,
                                        height=200)

        sub_layout = pm.columnLayout(adjustableColumn=True, parent=scroll_layout)

        for items in self.qss_files:
            print items
            self.qss_widget(qss_name=items, parent=sub_layout)
        self.namespace_widget(parent=layout)
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
        if sel_set_members:
            if [ i for i in selection if i in sel_set_members]:
                return sel_set
            else:
                return None
        else:
            msg = 'no quick selects found in scene'
            message.error(position="botRight", prefix="Error", message=msg, fadeStayTime=3.0, fadeOutTime=4.0)


class qss_data_obj():
    def __init__(self, qs_name="", qs_objects=[]):
        self.qs_name = qs_name
        self.qs_objects = qs_objects