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

    usage - to automatically add a bunch of commands for hotkeys
    import tb_keyCommands as tb_hotKeys
    tb_hotKeys.add_tbtools_commands()

*******************************************************************************
'''

import pymel.core as pm

from tb_hkey import tb_hkey

def make_command_list():

    command_list = []

    # keyframing tools
    cat = 'tbtools_keyframing'
    command_list.append(tb_hkey(name='smart_frame_curves', annotation='smart framing of keys',
                                category=cat, command = [ 'import tb_graphEditor as ge',
                                                         'reload(ge)',
                                                         'ge.graphEditor().smart_frame()' ]) )
    command_list.append(tb_hkey(name='match_tangent_start_to_end', annotation='',
                                category=cat, command = [ 'import key_mod as ky',
                                                         'reload(ky)',
                                                         'ky.keyTools().match(\"start\")']) )
    command_list.append(tb_hkey(name='match_tangent_end_to_start', annotation='',
                                category=cat, command = [ 'import key_mod as ky',
                                                         'reload(ky)',
                                                         'ky.keyTools().match(\"end\")']) )

    # camera tools
    cat = 'tbtools_cameras'
    command_list.append(tb_hkey(name='tracking_camera_track', annotation='creates/rebuilds a tracking camera to track your current selection',
                                category=cat, command = [ 'import tb_trackingCam as tc',
                                                         'reload (tc)',
                                                         'tc.track(\"tracker\")']) )
    command_list.append(tb_hkey(name='tracking_camera_update', annotation='updates the object tracked by the tracking camera, switches view',
                                category=cat, command = [ 'import tb_trackingCam as tc',
                                                         'reload (tc)',
                                                         'tc.track(\"retarget\",\"tracker\")']) )
    command_list.append(tb_hkey(name='tracking_camera_persp', annotation='swaps the view to the perspective camera, matching your current view',
                                category=cat, command = [ 'import tb_trackingCam as tc',
                                                         'reload (tc)',
                                                         'tc.track(\"persp\")']) )

    # viewport tools
    cat = 'tbtools_view'
    command_list.append(tb_hkey(name='ViewMode_Objects_Joints', annotation='',
                                category=cat, command = [ 'import tb_viewModes as vm',
                                                         'reload (vm)',
                                                         'vm.viewMode(\"joints\")']) )
    command_list.append(tb_hkey(name='ViewMode_Objects_Meshes', annotation='',
                                category=cat, command = [ 'import tb_viewModes as vm',
                                                         'reload (vm)',
                                                         'vm.viewMode(\"meshes\")']) )
    command_list.append(tb_hkey(name='ViewMode_Objects_All', annotation='',
                                category=cat, command = [ 'import tb_viewModes as vm',
                                                         'reload (vm)',
                                                         'vm.viewMode(\"allObj\")']) )

    # manipulator tools
    cat = 'tbtools_manipulators'
    command_list.append(tb_hkey(name='cycle_rotation', annotation='cycle the rotation mode',
                                category=cat, command = [ 'import tb_manipulators as tbm',
                                                         'reload (tbm)',
                                                         'tbm.manips().cycleRotation()']) )
    command_list.append(tb_hkey(name='cycle_translation', annotation='cycle the translation mode',
                                category=cat, command = [ 'import tb_manipulators as tbm',
                                                         'reload (tbm)',
                                                         'tbm.manips().cycleTranslation()']) )
    command_list.append(tb_hkey(name='cycle_object_selection_mask', annotation='cycle the selection mask',
                                category=cat, command = [ 'import tb_manipulators as tbm',
                                                         'reload (tbm)',
                                                         'tbm.manips().cycle_selection_mask()']) )
    command_list.append(tb_hkey(name='cycle_set_keyframe_type', annotation='cycle the setkey type',
                                category=cat, command = [ 'import tb_manipulators as tbm',
                                                         'reload (tbm)',
                                                         'tbm.manips().cycle_key_type()']) )
    command_list.append(tb_hkey(name='smooth_drag_timeline_on', annotation='timeslider tool with no frame snapping',
                                category=cat, command = [ 'import tb_timeDragger as td',
                                                         'reload (td)',
                                                         'td.drag(True)']) )
    command_list.append(tb_hkey(name='smooth_drag_timeline_off', annotation='timeslider tool with no frame snapping',
                                category=cat, command = [ 'import tb_timeDragger as td',
                                                         'reload (td)',
                                                         'td.drag(False)']) )
    return command_list


class hotkey_tool():
    def __init__(self):
        self.categories = [ "tb_tools", 'tbtools_view', 'tbtools_keyframing', 'tbtools_cameras', 'tbtools_manipulators' ]
        self.command_list = make_command_list()
        self.name_list = self.get_command_names()
        self.tb_commands = self.get_existing_commands()
        self.extra_commands = pm.optionVar.get('tb_extra_commands', '')
        self.remove_unneeded_ignore_entries()
        pass

    def update_commands(self):
        for commands in self.command_list:
            self.add_command(commands)
            
    def add_command(self, hkey=tb_hkey()):
        if not pm.runTimeCommand(hkey.name, exists=True):
            pm.runTimeCommand(hkey.name)

        pm.runTimeCommand(
            hkey.name,
            edit=True,
            annotation=hkey.annotation,
            category=hkey.category,
            commandLanguage=hkey.language,
            command=hkey.command)

    def remove_unneeded_ignore_entries(self):
        needed_ignore_names = []
        for items in self.extra_commands:
            if items in self.tb_commands:
                needed_ignore_names.append(items)

        pm.optionVar.pop('tb_extra_commands')
        for items in needed_ignore_names:
            pm.optionVar(stringValueAppend=('tb_extra_commands', items))


    def get_existing_commands(self):
        _commands = []
        existing_commands = pm.runTimeCommand(query=True, userCommandArray=True)

        # loop through existing commands
        for com in existing_commands:
            # filter out non tbtools commands
            if pm.runTimeCommand(com, query=True, category=True) in self.categories:
                _commands.append(com)
        return _commands


    def remove_bad_commands(self):
        commands_for_deletion = []
        for com in self.tb_commands:
            if com not in self.name_list:
                if com not in self.extra_commands:
                    commands_for_deletion.append(com)
                
        if commands_for_deletion:
            hotkey_cleanup(commands_to_delete=commands_for_deletion)

    def get_command_names(self):
        names = []
        for cmd in self.command_list:
            names.append(cmd.name)
        return names
        


    
class hotkey_cleanup():
    def __init__(self, commands_to_delete=[]):
        self.command_list = commands_to_delete
        self.showUI()
        pass

    def remove_hotkey(self, command_name, layout_name):
        pm.runTimeCommand(command_name, edit=True, delete=True)
        pm.deleteUI(layout_name)
    
    def ignore_hotkey(self, command_name, layout_name):
        pm.optionVar(stringValueAppend=('tb_extra_commands', command_name))
        pm.rowLayout(layout_name, edit=True, bgc=(0.2,0.6,0.2))
        
    def command_widget(self, command_name="", parent=""):
        rLayout = pm.rowLayout(numberOfColumns=4, adjustableColumn=2, parent=parent)
        pm.text(label="command:", parent=rLayout)
        pm.text(label=str(command_name), parent=rLayout)

        pm.button(label="keep", parent=rLayout, command=lambda *args : self.ignore_hotkey(command_name, rLayout))
        pm.button(label="delete", parent=rLayout, command=lambda *args : self.remove_hotkey(command_name, rLayout))

    def showUI(self):
        window = pm.window( title="hotkey check!")
        layout = pm.columnLayout(adjustableColumn=True )
        pm.text(font="boldLabelFont",label="Uknown or outdated commands")
        pm.text(label="")

        pm.text(label="your own commands saved in tbtools categories")
        pm.text(label="will show up here. If you wish to keep them,")
        pm.text(label="press the 'keep' button and they won't appear")
        pm.text(label="in this window again.")
        pm.text(label="")
        pm.text(label="If you didn't make it and it's here it means it")
        pm.text(label="is an old or outdated hotkey and should be removed")
        pm.text(label="")
                
        for items in self.command_list:
            self.command_widget(command_name=items, parent=layout)

        # pm.button( label='Delete all', parent=layout)
        pm.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') , parent=layout)
        pm.setParent( '..' )
        pm.showWindow(window)
