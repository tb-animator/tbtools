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
    tb_hotKeys.hotkey_tool().update_commands()

*******************************************************************************
'''

import pymel.core as pm

from tb_hkey import tb_hkey


def make_command_list():
    command_list = []

    # keyframing tools
    cat = 'tbtools_importExport'
    command_list.append(tb_hkey(name='mocapImporter', annotation='mocap import window',
                            category=cat, command=['import rig.mocapLinker.mocapImporter as mi',
                                                   'reload(mi)',
                                                   'mWindow = mi.mocapWindow(mi.mayaMainWindow())',
                                                   'mWindow.show()']))
    cat = 'tbtools_keyframing'
    command_list.append(tb_hkey(name='flatten_control', annotation='flattens the control out',
                                category=cat, command=['import tb_flatten as tbf',
                                                       'reload(tbf)',
                                                       'tbf.level()']))
    command_list.append(tb_hkey(name='lazy_cycle_anim', annotation='lazy_cycle_maker',
                                category=cat, command=['import animCycle.tb_cycler as tbs',
                                                       'reload(tbs)',
                                                       'tbs.cycler().go()']))
    command_list.append(tb_hkey(name='store_ctrl_transform', annotation='store object transform',
                                category=cat, command=['from tb_snaps import SnapTools',
                                                       'SnapTools().store_transform()']))
    command_list.append(tb_hkey(name='restore_ctrl_transform', annotation='restore object transform',
                                category=cat, command=['from tb_snaps import SnapTools',
                                                       'SnapTools().restore_transform()']))
    command_list.append(tb_hkey(name='snap_objects', annotation='snap selection',
                                category=cat, command=['from tb_snaps import SnapTools',
                                                       'SnapTools().snap_selection()']))
    command_list.append(tb_hkey(name='zero_translates', annotation='zero translation values',
                                category=cat, command=['import tb_manipulators as tbm',
                                                       'reload(tbm)',
                                                       'tbm.zeroes().zero_translates()']))
    command_list.append(tb_hkey(name='zero_rotates', annotation='zero rotation values',
                                category=cat, command=['import tb_manipulators as tbm',
                                                       'reload(tbm)',
                                                       'tbm.zeroes().zero_rotates()']))
    command_list.append(tb_hkey(name='zero_scales', annotation='zero scale values',
                                category=cat, command=['import tb_manipulators as tbm',
                                                       'reload(tbm)',
                                                       'tbm.zeroes().zero_scales()']))
    command_list.append(tb_hkey(name='smart_frame_curves', annotation='smart framing of keys, or focus on selection',
                                category=cat, command=['import tb_graphEditor as ge',
                                                       'reload(ge)',
                                                       'ge.graphEditor().smart_frame()']))
    command_list.append(
        tb_hkey(name='smart_open_graphEditor', annotation='smart framing of keys, and opens the graph editor',
                category=cat, command=['import tb_graphEditor as ge',
                                       'reload(ge)',
                                       'ge.graphEditor().open_graph_editor()']))
    command_list.append(tb_hkey(name='match_tangent_start_to_end', annotation='',
                                category=cat, command=['from tb_keyframe import key_mod',
                                                       'key_mod().match(\"start\")']))
    command_list.append(tb_hkey(name='match_tangent_end_to_start', annotation='',
                                category=cat, command=['from tb_keyframe import key_mod',
                                                       'key_mod().match(\"end\")']))
    command_list.append(
        tb_hkey(name='filter_channelBox', annotation='filters the current channelBox seletion in the graph editor',
                category=cat, command=['from tb_keyframe import channels',
                                       'channels().filterChannels()']))
    # push and pull
    command_list.append(
        tb_hkey(name='tb_pull_left', annotation='scale values down, from left',
                category=cat, command=['import tb_keyMod as tbkm',
                                       'reload(tbkm)',
                                       'tbkm.keyTools().push_and_pull(\"pull\", \"left\")']))
    command_list.append(
        tb_hkey(name='tb_pull_right', annotation='scale values down, from left',
                category=cat, command=['import tb_keyMod as tbkm',
                                       'reload(tbkm)',
                                       'tbkm.keyTools().push_and_pull(\"pull\", \"right\")']))
    command_list.append(
        tb_hkey(name='tb_push_left', annotation='scale values down, from left',
                category=cat, command=['import tb_keyMod as tbkm',
                                       'reload(tbkm)',
                                       'tbkm.keyTools().push_and_pull(\"push\", \"left\")']))
    command_list.append(
        tb_hkey(name='tb_push_right', annotation='scale values down, from right',
                category=cat, command=['import tb_keyMod as tbkm',
                                       'reload(tbkm)',
                                       'tbkm.keyTools().push_and_pull(\"push\", \"right\")']))
    command_list.append(
        tb_hkey(name='tb_negate_left', annotation='flip values, from left',
                category=cat, command=['import tb_keyMod as tbkm',
                                       'reload(tbkm)',
                                       'tbkm.keyTools().negate_keys(\"left\")']))
    command_list.append(
        tb_hkey(name='tb_negate_right', annotation='flip values, from right',
                category=cat, command=['import tb_keyMod as tbkm',
                                       'reload(tbkm)',
                                       'tbkm.keyTools().negate_keys(\"right\")']))


    # camera tools
    cat = 'tbtools_cameras'

    command_list.append(tb_hkey(name='tracking_camera_track',
                                annotation='creates/rebuilds a tracking camera to track your current selection',
                                category=cat, command=['import tb_trackingCam as tc',
                                                       'reload (tc)',
                                                       'tc.track(\"tracker\")']))
    command_list.append(tb_hkey(name='tracking_camera_update',
                                annotation='updates the object tracked by the tracking camera, switches view',
                                category=cat, command=['import tb_trackingCam as tc',
                                                       'reload (tc)',
                                                       'tc.track(\"retarget\",\"tracker\")']))
    command_list.append(tb_hkey(name='tracking_camera_persp',
                                annotation='swaps the view to the perspective camera, matching your current view',
                                category=cat, command=['import tb_trackingCam as tc',
                                                       'reload (tc)',
                                                       'tc.track(\"persp\")']))
    command_list.append(tb_hkey(name='updateTumble', annotation='update the camera tumble pivots',
                                category=cat, command=['try:',
                                                       '    tumbler.doIt()',
                                                       'except:',
                                                       '    import cameraTools.cameraCOI as COI',
                                                       '    reload(COI)',
                                                       '    tumbler = COI.tumbler()',
                                                       '    tumbler.doIt()',
                                                       ]))

    # viewport tools
    cat = 'tbtools_view'
    command_list.append(tb_hkey(name='ViewMode_xray_joints', annotation='',
                                category=cat, command=['import tb_viewModes as vm',
                                                       'reload (vm)',
                                                       'vm.toggleXrayJoints()']))
    command_list.append(tb_hkey(name='ViewMode_xray', annotation='',
                            category=cat, command=['import tb_viewModes as vm',
                                                   'reload (vm)',
                                                   'vm.toggleXray()']))
    command_list.append(tb_hkey(name='ViewMode_Objects_Joints', annotation='',
                                category=cat, command=['import tb_viewModes as vm',
                                                       'reload (vm)',
                                                       'vm.viewMode(\"joints\")']))
    command_list.append(tb_hkey(name='ViewMode_Objects_Meshes', annotation='',
                                category=cat, command=['import tb_viewModes as vm',
                                                       'reload (vm)',
                                                       'vm.viewMode(\"meshes\")']))
    command_list.append(tb_hkey(name='ViewMode_Objects_All', annotation='',
                                category=cat, command=['import tb_viewModes as vm',
                                                       'reload (vm)',
                                                       'vm.viewMode(\"allObj\")']))
    command_list.append(tb_hkey(name='toggle_isolate_selection', annotation='',
                                category=cat, command=['import tb_isolator as tbi',
                                                       'reload(tbi)',
                                                       'tbi.isolator().toggle_isolate()']))
    command_list.append(
        tb_hkey(name='incremental_playblast_quicktime', annotation='incrememnt and save playblasts in mov',
                category=cat, command=['import tb_playblast as tbp',
                                       'tbp.make_playblast(type="mov")']))
    command_list.append(tb_hkey(name='incremental_playblast_avi', annotation='incrememnt and save playblasts in avi',
                                category=cat, command=['import tb_playblast as tbp',
                                                       'tbp.make_playblast(type="avi")']))
    command_list.append(tb_hkey(name='toggle_playback_tool',
                                annotation='does fancy playback toggling',
                                category=cat, command=['try:',
                                                       '	player.playPause()',
                                                       'except:',
                                                       '	import tb_playback as tbp',
                                                       '	reload(tbp)',
                                                       '	player = tbp.playback()',
                                                       '	player.playPause()',
                                                       ]))
    command_list.append(tb_hkey(name='toggle_playback_viewport',
                                annotation='does fancy playback toggling viewport modes',
                                category=cat, command=['try:',
                                                       '	player.toggleAll()',
                                                       'except:',
                                                       '	import tb_playback as tbp',
                                                       '	reload(tbp)',
                                                       '	player = tbp.playback()',
                                                       '	player.toggleAll()',
                                                       ]))
    command_list.append(tb_hkey(name='flip_playback',
                                annotation='does fancy playback toggling',
                                category=cat, command=['try:',
                                                       '	player.playPause(flip=True)',
                                                       'except:',
                                                       '	import tb_playback as tbp',
                                                       '	reload(tbp)',
                                                       '	player = tbp.playback()',
                                                       '	player.playPause(flip=True)',
                                                       ]))
    command_list.append(tb_hkey(name='shift_time_range_start', annotation='',
                                category=cat, command=['try:',
                                                       '	timeline().shift_start()',
                                                       'except:',
                                                       '	from tb_timeline import timeline',
                                                       '	timeline().shift_start()',
                                                       ]))
    command_list.append(tb_hkey(name='shift_time_range_end', annotation='',
                                category=cat, command=['try:',
                                                       '	timeline().shift_end()',
                                                       'except:',
                                                       '	from tb_timeline import timeline',
                                                       '	timeline().shift_end()',
                                                       ]))
    command_list.append(tb_hkey(name='crop_time_range_start', annotation='',
                                category=cat, command=['try:',
                                                       '	timeline().crop()',
                                                       'except:',
                                                       '	from tb_timeline import timeline',
                                                       '	timeline().crop()',
                                                       ]))
    command_list.append(tb_hkey(name='crop_time_range_end', annotation='',
                                category=cat, command=['try:',
                                                       '	timeline().crop(start=False)',
                                                       'except:',
                                                       '	from tb_timeline import timeline',
                                                       '	timeline().crop(start=False)',
                                                       ]))
    command_list.append(tb_hkey(name='skip_forward', annotation='',
                                category=cat, command=['import tb_timeline as tbt',
                                                       'reload(tbt)',
                                                       'tbt.skip(mode=1)'
                                                       ]))
    command_list.append(tb_hkey(name='skip_backward', annotation='',
                                category=cat, command=['import tb_timeline as tbt',
                                                       'reload(tbt)',
                                                       'tbt.skip(mode=-1)'
                                                       ]))
    # constraint/bake tools
    cat = 'tbtools_constraints'
    command_list.append(tb_hkey(name='bakeToLocator', annotation='constrain to object to locator',
                                category=cat, command=['import cake.ezBake as ezb',
                                                       'reload(ezb)',
                                                       'ezb.bake_to_locator(constrain=True, orientOnly=False)']))
    command_list.append(tb_hkey(name='bakeToLocatorRotation', annotation='constrain to object to locator',
                                category=cat, command=['import cake.ezBake as ezb',
                                                       'reload(ezb)',
                                                       'ezb.bake_to_locator(constrain=True, orientOnly=True)']))
    command_list.append(tb_hkey(name='simpleConstraintOffset', annotation='constrain to objects with offset',
                                category=cat, command=['import cake.ezBake as ezb',
                                                       'reload(ezb)',
                                                       'ezb.parentConst(constrainGroup=False, offset=True, postBake=False)']))
    command_list.append(tb_hkey(name='simpleConstraintNoOffset', annotation='constrain to objects with NO offset',
                                category=cat, command=['import cake.ezBake as ezb',
                                                       'reload(ezb)',
                                                       'ezb.parentConst(constrainGroup=False, offset=False, postBake=False)']))
    command_list.append(
        tb_hkey(name='simpleConstraintOffsetPostBake', annotation='constrain to objects with offset - post baked',
                category=cat, command=['import cake.ezBake as ezb',
                                       'reload(ezb)',
                                       'ezb.parentConst(constrainGroup=False, offset=True, postBake=True)']))
    command_list.append(
        tb_hkey(name='simpleConstraintNoOffsetPostBake', annotation='constrain to objects with NO offset - post baked',
                category=cat, command=['import cake.ezBake as ezb',
                                       'reload(ezb)',
                                       'ezb.parentConst(constrainGroup=False, offset=False, postBake=True)']))
    command_list.append(tb_hkey(name='simpleConstraintOffsetPostBakeReverse',
                                annotation='constrain to objects with offset - post baked, constraint reversed',
                                category=cat, command=['import cake.ezBake as ezb',
                                                       'reload(ezb)',
                                                       'ezb.parentConst(constrainGroup=False, offset=True, postBake=True, postReverseConst=True)']))
    command_list.append(tb_hkey(name='simpleConstraintNoOffsetPostBakeReverse',
                                annotation='constrain to objects with NO offset - post baked, constraint reversed',
                                category=cat, command=['import cake.ezBake as ezb',
                                                       'reload(ezb)',
                                                       'ezb.parentConst(constrainGroup=False, offset=False, postBake=True, postReverseConst=True)']))

    # manipulator tools
    cat = 'tbtools_manipulators'
    command_list.append(tb_hkey(name='cycle_rotation', annotation='cycle the rotation mode',
                                category=cat, command=['import tb_manipulators as tbm',
                                                       'reload (tbm)',
                                                       'tbm.manips().cycleRotation()']))
    command_list.append(tb_hkey(name='cycle_translation', annotation='cycle the translation mode',
                                category=cat, command=['import tb_manipulators as tbm',
                                                       'reload (tbm)',
                                                       'tbm.manips().cycleTranslation()']))
    command_list.append(tb_hkey(name='cycle_object_selection_mask', annotation='cycle the selection mask',
                                category=cat, command=['import tb_manipulators as tbm',
                                                       'reload (tbm)',
                                                       'tbm.manips().cycle_selection_mask()']))
    command_list.append(tb_hkey(name='cycle_set_keyframe_type', annotation='cycle the setkey type',
                                category=cat, command=['import tb_manipulators as tbm',
                                                       'reload (tbm)',
                                                       'tbm.manips().cycle_key_type()']))
    command_list.append(tb_hkey(name='smooth_drag_timeline_on', annotation='timeslider tool with no frame snapping',
                                category=cat, command=['try:',
                                                       '	my_td.drag(True)',
                                                       'except:',
                                                       '	from tb_timeDragger import timeDragger',
                                                       '	my_td = timeDragger()',
                                                       '	my_td.drag(True)',
                                                       ]))
    command_list.append(
        tb_hkey(name='smooth_drag_timeline_off', annotation='set to same hotkey as ON, but tick release',
                category=cat, command=['try:',
                                       '	my_td.drag(False)',
                                       'except:',
                                       '	from tb_timeDragger import timeDragger',
                                       '	my_td = timeDragger()',
                                       '	my_td.drag(False)',
                                       ]))
    command_list.append(tb_hkey(name='step_drag_timeline_on', annotation='timeslider tool with no frame snapping',
                                category=cat, command=['try:',
                                                       '	my_td.stepDrag(True)',
                                                       'except:',
                                                       '	from tb_timeDragger import timeDragger',
                                                       '	my_td = timeDragger()',
                                                       '	my_td.stepDrag()',
                                                       ]))
    command_list.append(
        tb_hkey(name='step_drag_timeline_off', annotation='set to same hotkey as ON, but tick release',
                category=cat, command=['try:',
                                       '	my_td.stepDrag(False)',
                                       'except:',
                                       '	from tb_timeDragger import timeDragger',
                                       '	my_td = timeDragger()',
                                       '	my_td.stepDrag(state=False)',
                                       ]))
    cat = 'tbtools_selection'
    # all curve selector
    command_list.append(tb_hkey(name='select_all_anim_curves', annotation='',
                                category=cat, command=['import tb_selections as tb_sel',
                                                       'reload (tb_sel)',
                                                       'tb_sel.select_all_non_referenced_curves()']))
    # char set selector
    command_list.append(tb_hkey(name='select_character_set_objs', annotation='',
                                category=cat, command=['import tb_selections as tb_sel',
                                                       'reload (tb_sel)',
                                                       'tb_sel.select_cheracter_set()']))
    # quick selection set - select
    command_list.append(tb_hkey(name='select_quick_select_set_objs', annotation='',
                                category=cat, command=['import tb_selections as tb_sel',
                                                       'reload (tb_sel)',
                                                       'tb_sel.quick_selection().qs_select()']))
    command_list.append(tb_hkey(name='quick_select_load_window', annotation='load quick selects from saved files',
                                category=cat, command=['import tb_selections as tb_sel',
                                                       'reload (tb_sel)',
                                                       'tb_sel.quick_selection().restore_qs_from_dir()']))
    command_list.append(tb_hkey(name='save_quick_selects_to_file', annotation='load quick selects from saved files',
                                category=cat, command=['import tb_selections as tb_sel',
                                                       'reload (tb_sel)',
                                                       'tb_sel.quick_selection().save_qs_to_file()']))
    command_list.append(tb_hkey(name='create_quick_select_set', annotation='load quick selects from saved files',
                                category=cat, command=['import tb_selections as tb_sel',
                                                       'reload (tb_sel)',
                                                       'tb_sel.quick_selection().create_qs_set()']))
    # pickwalk (multi)
    command_list.append(tb_hkey(name='pickwalk_up', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(up=True)']))
    command_list.append(tb_hkey(name='pickwalk_down', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(down=True)']))
    command_list.append(tb_hkey(name='pickwalk_left', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(left=True)']))
    command_list.append(tb_hkey(name='pickwalk_right', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(right=True)']))
    # pickwalk multi add
    command_list.append(tb_hkey(name='pickwalk_up_add', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(up=True, add=True)']))
    command_list.append(tb_hkey(name='pickwalk_down_add', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(down=True, add=True)']))
    command_list.append(tb_hkey(name='pickwalk_left_add', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(left=True, add=True)']))
    command_list.append(tb_hkey(name='pickwalk_right_add', annotation='',
                                category=cat, command=['from tb_selections import pickwalker',
                                                       'pickwalker().walk(right=True, add=True)']))
    return command_list


class hotkey_tool():
    def __init__(self):
        self.categories = ["tb_tools",
                           'tbtools_view',
                           'tbtools_keyframing',
                           'tbtools_cameras',
                           'tbtools_constraints',
                           'tbtools_manipulators',
                           'tbtools_selection']
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
        if self.extra_commands and self.tb_commands:
            for items in self.extra_commands:
                if items in self.tb_commands:
                    needed_ignore_names.append(items)

        pm.optionVar.pop('tb_extra_commands')
        for items in needed_ignore_names:
            pm.optionVar(stringValueAppend=('tb_extra_commands', items))


    def get_existing_commands(self):
        _commands = []
        existing_commands = pm.runTimeCommand(query=True, userCommandArray=True)

        if existing_commands:
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
        pm.rowLayout(layout_name, edit=True, bgc=(0.2, 0.6, 0.2))

    def command_widget(self, command_name="", parent=""):
        rLayout = pm.rowLayout(numberOfColumns=4, adjustableColumn=2, parent=parent)
        pm.text(label="command:", parent=rLayout)
        pm.text(label=str(command_name), parent=rLayout)

        pm.button(label="keep", parent=rLayout, command=lambda *args: self.ignore_hotkey(command_name, rLayout))
        pm.button(label="delete", parent=rLayout, command=lambda *args: self.remove_hotkey(command_name, rLayout))

    def showUI(self):
        window = pm.window(title="hotkey check!")
        layout = pm.columnLayout(adjustableColumn=True)
        pm.text(font="boldLabelFont", label="Uknown or outdated commands")
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
        pm.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), parent=layout)
        pm.setParent('..')
        pm.showWindow(window)
