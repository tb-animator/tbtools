__author__ = 'Tom'
import pymel.core as pm
import tb_messages as tb_msg



def intEntered(name, *args):
    pm.optionVar(intValue=(str(name), args[0]))


class folder_picker():
    def __init__(self):
        self.main_layout = pm.formLayout()
        self.layout = pm.rowLayout(numberOfColumns=3,
                                   adjustableColumn=2,
                                   columnAlign=[1, 'both'],
                                   columnAttach2=['both', 'left'],
                                   parent=self.main_layout
                                   )
        self.label = pm.text(parent=self.layout)
        self.label2 = pm.text(parent=self.main_layout)
        self.folder_field = pm.textField(parent=self.layout)
        self.button = pm.symbolButton(parent=self.layout)
        pass

    def create(self, parent="", label="", option_variable="", top_form="", top_control=""):
        pm.formLayout(self.main_layout, edit=True, parent=parent)
        pm.text(self.label2, edit=True, label=label)
        pm.rowLayout(self.layout,
                     parent=self.main_layout
                     )
        pm.text(self.label, edit=True, label="")
        pm.textField(self.folder_field,
                     edit=True,
                     text=pm.optionVar.get(option_variable, 'c:/qss/')
                     )
        pm.symbolButton(self.button,
                        edit=True,
                        image="navButtonBrowse.png",
                        command=lambda *args: self.set_option_dir(option_variable, self.folder_field, args[0])
                        )

        if top_control:
            pm.formLayout(
                top_form,
                edit=True,
                attachControl=[self.main_layout, 'top', 0, top_control],
                attachForm=[[self.main_layout, 'left', 0],
                            [self.main_layout, 'right', 0]]
            )

        elif top_form:
            pm.formLayout(
                top_form,
                edit=True,
                attachForm=[[self.main_layout, 'top', 0],
                            [self.main_layout, 'left', 0],
                            [self.main_layout, 'right', 0]]
            )

        # self.attach_form(self.layout, self.main_layout)
        FormAttach().attach(self.layout, self.main_layout)
        return self.main_layout

    @staticmethod
    def pin_to_top(attach_form, form):
        pass

    @staticmethod
    def attach_form(attach_form, form):
        af = [[attach_form, 'top', 16],
              [attach_form, 'left', 16],
              [attach_form, 'right', 16],
              [attach_form, 'bottom', 16]
              ]
        pm.formLayout(
            form,
            edit=True,
            attachForm=af
        )

    @staticmethod
    def set_option_dir(_name, _field, *args):
        _filter = '*.dir'
        _start_dir = pm.optionVar.get(_name, pm.workspace(query=True, directory=True))
        _result = pm.fileDialog2(startingDirectory=_start_dir,
                                 fileMode=3,
                                 fileFilter=_filter,
                                 dialogStyle=1,
                                 okCaption='pick')
        if _result:
            pm.optionVar(stringValue=(_name, _result[0] + "/"))
            pm.textField(_field, edit=True, text=_result[0])
        return _name


class positionWidget():
    def __init__(self):
        self.positions = tb_msg.Message().positions
        pass

    def changed(self, name, *args):
        pm.optionVar(stringValue=(str(name), args[0]))

    def create(self, name='', label=''):
        option_Menu = pm.optionMenu(name,
                                    label=label,
                                    changeCommand=lambda *args: self.changed(name, args[0])
                                    )
        for pos in tb_msg.Message().positions:
            pm.menuItem(label=pos)
        print name
        default_value = pm.optionVar.get(name, 'topLeft')
        pm.optionMenu(option_Menu, edit=True, select=self.positions.index(default_value) + 1)
        # return option_Menu


class checkBox_group():
    def __init__(self, columns=3):
        self.main_layout = pm.formLayout()
        self.sub_frameLayout = pm.frameLayout(parent=self.main_layout,
                                              labelVisible=False,
                                              borderStyle='etchedIn'
                                              )
        self.sub_formLayout = pm.formLayout(parent=self.sub_frameLayout)
        self.layout = None
        self.label = pm.text(parent=self.main_layout)
        pm.formLayout(
                self.main_layout,
                edit=True,
                attachForm=[[self.sub_frameLayout, 'top', 24],
                            [self.sub_frameLayout, 'left', 8],
                            [self.sub_frameLayout, 'right', 12],
                            [self.sub_frameLayout, 'bottom', 8]]
        )

        pm.setParent(self.sub_formLayout)
        pass

    class cBox():
        def _optionCheckBox_single(self, name="", label="", annotation="", variable="", defaultValue=False):
            print name, pm.optionVar.get(variable)
            _checkBox = pm.checkBox(name, label=label,
                                    value=pm.optionVar.get(variable, defaultValue),
                                    annotation=annotation,
                                    align="right",
                                    changeCommand=lambda *args: self.checkBox_pressed(name, args[0])
                                    )
            # hacky way to save the value of the checkbox back to the option var
            pm.optionVar(intValue=(variable, pm.optionVar.get(variable, defaultValue)))
            return _checkBox

        @staticmethod
        def checkBox_pressed(name, *args):
            pm.optionVar(intValue=(str(name), args[0]))


        def _optionCheckBox(self, name="", label="", annotation="", variable=""):
            var_list = pm.optionVar.get(variable)
            if var_list:
                value = name in var_list
            else:
                value = False
            _checkBox = pm.checkBox(name, label=label,
                                    value=value,
                                    annotation=annotation,
                                    changeCommand=lambda *args: self.checkBox_pressed_array(variable, name, args[0])
                                    )
            return _checkBox

        @staticmethod
        def checkBox_pressed_array(variable, name, state):
            vars = pm.optionVar.get(variable, [''])
            if state:
                # checkbox ticked, add option to list
                if name not in vars:
                    # not already set in list so add it
                    pm.optionVar(stringValueAppend=(variable, name))
            else:
                # checkbox un ticked, remove from list
                if name in vars:
                    pm.optionVar(removeFromArray=(variable, vars.index(name)))


    def create(self, parent="", label="", columns=3, optionList=[], variable="", positionMenu="", positionLabel="",
               messageMenu="", top_form="", top_control="", intField="", intFieldLabel=""):
        pm.formLayout(self.main_layout, edit=True, parent=parent)
        pm.text(self.label, edit=True, label=label)
        if positionMenu:
            offset = 1
        cLayout = pm.rowLayout(numberOfColumns=3,
                               adjustableColumn=2,
                               parent=self.sub_formLayout,
                               columnAlign=[3, 'right'])

        FormAttach().fill_right(cLayout, self.sub_formLayout)
        FormAttach().fill_left(cLayout, self.sub_formLayout)

        self.layout = pm.rowColumnLayout(numberOfColumns=columns,
                                         columnAlign=[1, 'both'],
                                         parent=cLayout
                                         )
        for options in optionList:
            self.cBox()._optionCheckBox(variable=variable,
                                        name=options,
                                        label=options)
        if intField:
            pm.text(label=intFieldLabel)
            pm.intField(parent=self.layout,
                        width=64,
                        value=pm.optionVar.get(intField, 2),
                        changeCommand=lambda *args: intEntered(intField, args[0]))


        # spacer
        pm.text(label="", parent=cLayout)

        if positionMenu or messageMenu:
            # make a rowColumn layout to put our label and option box in nicely
            pm.setParent(cLayout)
            pm.rowColumnLayout(numberOfColumns=2, columnOffset=(2, "right", 20))
            pm.text(label="inView message")
            self.cBox()._optionCheckBox_single(variable=variable + "_msg",
                                               name=variable + "_msg",
                                               defaultValue=True)

            if positionMenu:
                pm.text(label=positionLabel)
                positionWidget().create(name=positionMenu)

        if top_control:
            pm.formLayout(
                top_form,
                edit=True,
                attachControl=[self.main_layout, 'top', 0, top_control],
                attachForm=[[self.main_layout, 'left', 8],
                            [self.main_layout, 'right', 8]]
            )

        elif top_form:
            pm.formLayout(
                top_form,
                edit=True,
                attachForm=[[self.main_layout, 'top', 24],
                            [self.main_layout, 'left', 8],
                            [self.main_layout, 'right', 8]]
            )




        return self.main_layout

class FormAttach():
    @staticmethod
    def attach(attach_form, form):
        af = [[attach_form, 'top', 16],
              [attach_form, 'left', 12],
              [attach_form, 'right', 12],
              [attach_form, 'bottom', 12]
              ]
        pm.formLayout(
            form,
            edit=True,
            attachForm=af
        )

    @staticmethod
    def fill_right(attach_form, form):
        af = [[attach_form, 'right', 12]]
        pm.formLayout(
            form,
            edit=True,
            attachForm=af
        )

    @staticmethod
    def fill_left(attach_form, form):
        af = [[attach_form, 'left', 12]]
        pm.formLayout(
            form,
            edit=True,
            attachForm=af
        )

    @staticmethod
    def stretch_down(attach_form, form):
        af = [[form, 'bottom', 12 ]]
        pm.formLayout(
            attach_form,
            edit=True,
            attachForm=af
        )


    @staticmethod
    def pin_under(attach_form, form_a, form_b):
        af = [[form_a, 'top', 12, form_b]]
        pm.formLayout(
            attach_form,
            edit=True,
            attachControl=af
        )
