__author__ = 'tom.bailey'
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

*******************************************************************************
'''
import maya.cmds as cmds
import maya.mel as mel
import tb_UI as tb_UI
import pymel.core as pm
from tb_timeDragger import timeDragger
from tb_manipulators import manips

reload(tb_UI)

if not pm.optionVar(exists='playblast_folder'):
    pm.optionVar(stringValue=('playblast_folder', "c:"))


def buttonPressed(name, *args):
    if args[0]:
        _val = 1
    else:
        _val = 2
    pm.optionVar(intValue=(str(name), _val))


def checkBox_pressed(name, *args):
    pm.optionVar(intValue=(str(name), args[0]))


def set_option_dir(_name, _field, *args):
    _filter = '*.dir'
    _start_dir = pm.optionVar[_name]
    _result = pm.fileDialog2(startingDirectory=_start_dir,
                             fileMode=3,
                             fileFilter=_filter,
                             dialogStyle=1,
                             okCaption='pick')[0]
    pm.optionVar(stringValue=(_name, _result + "/"))
    pm.textField(_field, edit=True, text=_result)
    return _name


def intEntered(name, *args):
    pm.optionVar(intValue=(str(name), args[0]))


def showUI():
    """A function to instantiate the pose manager window"""
    return anim_optionWindow.showUI()


class anim_optionWindow(object):
    @classmethod
    def showUI(cls):
        """A function to instantiate the pose manager window"""
        win = cls()
        win.create()
        return win

    def __init__(self):
        self.icon_path = ""
        self.titleImage = "option_top.png"
        self.titleImage_hvr = "option_top.png"
        self.reminder_img = "arrow.png"
        self.curve_btn_img = "curves.png"
        self.transform_btn_img = "transform.png"
        self.camera_btn_img = "tb_camera.png"

        # dictionary for category layouts
        self.categories = {}

        self.window = 'anim_option_win'
        self.bgc = [72.0 / 255.0, 79.0 / 255.0, 89.0 / 255.0]
        self._width = 600
        self._height = 450
        self._sm_margin = 4
        self._lrg_margin = 28
        self.optionLayouts = []

        # option variables
        self.translate_optionVars = manips().translate_modes

    def create(self):
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)

        self.window = pm.window(self.window, title='Animation options',
                                width=self._width,
                                height=self._height,
                                sizeable=True)
        if pm.uiTemplate('animUI_template', exists=True):
            pm.deleteUI('animUI_template', uiTemplate=True)

        pm.uiTemplate('animUI_template')

        cmds.button(defineTemplate='animUI_template', width=100, height=40, align='left')
        cmds.frameLayout(defineTemplate='animUI_template',
                         borderVisible=True,
                         labelVisible=True,
                         )
        cmds.textScrollList(defineTemplate='animUI_template',
                            backgroundColor=self.bgc
                            )
        self._form_layout = pm.formLayout()
        self.titleImage = pm.image(image=self.titleImage,
                                            width=self._width,
                                            height=75)
        # apply ui template
        pm.setUITemplate('animUI_template', pushTemplate=True)
        # build main category form
        self._menu_category(self._form_layout)

        # key options layout
        self.optionLayouts.append(self._keys_dialog_menu(self._form_layout))

        # manipulator options
        self.optionLayouts.append(self._manipulator_menu(self._form_layout))

        # add the file options menu
        self.optionLayouts.append(self._file_dialog_menu(self._form_layout))

        # revert ui template
        pm.setUITemplate(popTemplate=True)


        # attach frames to main form
        ac = []
        af = []
        # attach header image
        af.append([self.titleImage, 'top', 0])
        af.append([self.titleImage, 'left', self._sm_margin])
        af.append([self.titleImage, 'right', self._sm_margin])
        # attach left hand category menu
        ac.append([self._cat_layout, 'top', 0, self.titleImage])
        af.append([self._cat_layout, 'left', self._sm_margin])
        af.append([self._cat_layout, 'bottom', self._sm_margin])
        cmds.formLayout(
            self._form_layout, e=True,
            attachControl=ac, attachForm=af
        )
        # loop through the layouts
        self.attach_main_forms(main_layout=self._form_layout,
                               layouts=self.optionLayouts,
                               top=self.titleImage,
                               left=self._cat_layout)


        self.category_selected("manips_op")
        self.window.show()

    def attach_main_forms(self, main_layout, layouts=[], top=str(), left=str(), right=str(), bottom=str(),
                          margin=int(4)):
        for _form in layouts:
            ac = []
            af = []

            ac.append([str(_form), 'top', 0, top])
            ac.append([str(_form), 'left', 0, left])
            af.append([str(_form), 'right', margin])
            af.append([str(_form), 'bottom', margin])

            pm.formLayout(
                main_layout,
                edit=True,
                attachControl=ac,
                attachForm=af
            )

    def category_selected(self, _name):
        current = self.categories[_name]
        for keys in self.categories:
            pm.frameLayout(self.categories[keys], edit=True, manage=(keys == _name))


    def _rmb_menu(self, _parent):
        self._rmb_layout = pm.frameLayout(label="Right click Menu options",
                                          width=self._width - 16,
                                          collapsable=True,
                                          collapse=True,
                                          parent=_parent)

    def _optionCheckBox(self, _name, _label, _annotation):
        _checkBox = pm.checkBox(_name, label=_label,
                                value=optionVar(query=_name),
                                annotation=_annotation,
                                changeCommand=lambda *args: checkBox_pressed(_name, args[0])
                                )
        return _checkBox

    def _categoryButton(self, name="", width=int(64), height=int(64), icon="circle.png", parent=""):
        _button = pm.symbolButton(annotation=name,
                                  image=icon,
                                  parent=parent,
                                  width=width,
                                  height=height,
                                  command=lambda *args: self.category_selected(name)
                                  )
        return _button

    def _optionRadioButton(self, _name, _label, _labelArray, _annotation):
        _button = pm.radioButtonGrp(_name, numberOfRadioButtons=2,
                                    label=_label,
                                    select=pm.optionVar[_name],
                                    annotation=_annotation,
                                    labelArray2=_labelArray,
                                    adjustableColumn=1,
                                    columnAttach=[1, 'left', 0],
                                    changeCommand1=lambda *args: buttonPressed(_name, args[0]))
        return _button

    def _int_option(self, _name, _label):
        _field = pm.intField(_name,
                             value=pm.optionVar(query=_name),
                             enterCommand=lambda *args: intEntered(_name, args[0]))
        return _field

    # stupid fill out a form thing
    @staticmethod
    def attach_form(attach_form, form):
        af = []
        af.append([attach_form, 'top', 0])
        af.append([attach_form, 'left', 0])
        af.append([attach_form, 'right', 0])
        af.append([attach_form, 'bottom', 0])
        pm.formLayout(
            form,
            edit=True,
            attachForm=af
        )


    def _menu_category(self, _parent):
        self._cat_layout = pm.columnLayout()
        self._cat_form = pm.formLayout()
        file_option_btn = self._categoryButton(name="file_op", icon='folder.png', parent=self._cat_layout)
        keys_option_btn = self._categoryButton(name="keys_op", icon=self.curve_btn_img, parent=self._cat_layout)
        manips_option_btn = self._categoryButton(name="manips_op", icon=self.transform_btn_img, parent=self._cat_layout)
        # viewport_option_btn = self._categoryButton(name="view_op", icon=self.camera_btn_img, parent=self._cat_layout)

        pm.setParent(_parent)


    def _file_dialog_menu(self, _parent):
        self._file_layout = pm.frameLayout(label="File settings", bv=False)
        self._file_form = pm.formLayout()

        _dialogStyle = ['OS native', 'Maya default']
        '''
        playblast_folder_picker = tb_UI.folder_picker().create(parent=self._file_form,
                                                               label="playblast",
                                                               option_variable='tb_playblast_folder',
                                                               top_form=self._file_form
                                                               )
        '''
        selections_folder_picker = tb_UI.folder_picker().create(parent=self._file_form,
                                                                label="quick select save directory",
                                                                option_variable='tb_qs_folder',
                                                                #top_control=playblast_folder_picker,
                                                                top_form=self._file_form
                                                                )

        pm.setParent(_parent)
        self.categories["file_op"] = self._file_layout
        return self._file_layout

    def _manipulator_menu(self, _parent):
        _manip_layout = pm.frameLayout(label="manipulator settings", bv=False)
        _manip_form = pm.formLayout()
        _dialogStyle = ['OS native', 'Maya default']
        # _manip_columns = pm.columnLayout(columnAlign='center', bgc=(0.5,0.2,0.6))

        translate_options = tb_UI.checkBox_group().create(label="cycle translate tool options",
                                                          parent=_manip_form,
                                                          variable=manips().translate_optionVar,
                                                          columns=4,
                                                          optionList=manips().translate_modes,
                                                          positionMenu=manips().translate_messageVar,
                                                          positionLabel=manips().translate_messageLabel,
                                                          messageMenu=True,
                                                          top_form=_manip_form
                                                          )

        rotate_options = tb_UI.checkBox_group().create(label="cycle rotate tool options",
                                                       parent=_manip_form,
                                                       variable=manips().rotate_optionVar,
                                                       columns=4,
                                                       optionList=manips().rotate_modes,
                                                       positionMenu=manips().rotate_messageVar,
                                                       positionLabel=manips().rotate_messageLabel,
                                                       messageMenu=True,
                                                       top_control=translate_options,
                                                       top_form=_manip_form
                                                       )

        time_drag_options = tb_UI.checkBox_group().create(label="smooth drag tool options",
                                                       parent=_manip_form,
                                                       variable=timeDragger().optionVar,
                                                       columns=4,
                                                       optionList=timeDragger().modes,
                                                       positionMenu=timeDragger().messagePos,
                                                       positionLabel="message position",
                                                       messageMenu=True,
                                                       top_control=rotate_options,
                                                       top_form=_manip_form
                                                       )

        tb_UI.FormAttach().attach(_manip_layout, self._form_layout)


        pm.setParent(_parent)
        self.categories["manips_op"] = _manip_layout
        return _manip_layout

    def _keys_dialog_menu(self, _parent):
        _keys_layout = pm.frameLayout(label="keyframe settings", bv=False)
        _keys_form = pm.formLayout()

        keyframe_options = tb_UI.checkBox_group().create(label="cycle keyframe type options",
                                                       parent=_keys_form,
                                                       variable=manips().key_optionVar,
                                                       columns=4,
                                                       optionList=manips().key_modes,
                                                       positionMenu=manips().key_messageVar,
                                                       positionLabel=manips().key_messageLabel,
                                                       messageMenu=True,
                                                       top_form=_keys_form
                                                       )


        tb_UI.FormAttach().attach(_keys_layout, self._form_layout)


        pm.setParent(_parent)
        self.categories["keys_op"] = _keys_layout
        return _keys_layout
