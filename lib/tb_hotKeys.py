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
    import tb_hotKeys as tb_hotKeys
    tb_hotKeys.add_tbtools_commands()

*******************************************************************************
'''

import pymel.core as pm


def add_command(_name, _annotation, _category, _language, _command):
    if not pm.runTimeCommand(_name, exists=True):
        pm.runTimeCommand(
            _name,
            annotation=_annotation,
            category=_category,
            commandLanguage=_language,
            command=_command)
    else:
        pm.runTimeCommand(
            _name,
            edit=True,
            annotation=_annotation,
            category=_category,
            commandLanguage=_language,
            command=_command)


def add_tbtools_commands():
    ## command to add all hotkey commands to the hotkey editor
    # import tb_hotKeys as tb_hotKeys
    # tb_hotKeys.add_tbtools_commands()
    #
    _category = 'tb_tools'
    _py = 'python'
    _mel = 'mel'
    _commands = []

    _category = 'tb_tools_keyframing'
    _commands.append(['graphEditor_frame', 'smart framing of keys', _category, 'python',
                      'import animation.apps.graphEditor.NT_graphEditor as ge\nreload(ge)\nge.graphEditor().smart_frame()'])

    # match start to end
    _commands.append(['match_start_to_end', '', _category, 'python',
                      'import animation.apps.key_mod as ky\nreload(ky)\nky.keyTools().match(\"start\")'])
    # match end to start
    _commands.append(['match_end_to_start', '', _category, 'python',
                      'import animation.apps.key_mod as ky\nreload(ky)\nky.keyTools().match(\"end\")'])

    _category = 'tbtools_cameras'

    _commands.append(
        ['tracker_track', 'creates/rebuilds a tracking camera to track your current selection', _category, 'python',
         'import trackingCam as tc\nreload (tc)\ntc.track(\"tracker\")'])
    _commands.append(
        ['tracker_update', 'updates the object tracked by the tracking camera, switches view', _category, 'python',
         'import trackingCam as tc\nreload (tc)\ntc.track(\"newTarget\",\"tracker\")'])
    _commands.append(
        ['tracker_persp', 'swaps the view to the perspective camera, matching your current view', _category, 'python',
         'import trackingCam as tc\nreload (tc)\ntc.track(\"persp\")'])

    _category = 'tbtools_view'

    _commands.append(
        ['View_Objects_Joints', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"joints\")'])
    _commands.append(
        ['View_Objects_Meshes', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"meshes\")'])
    _commands.append(
        ['View_Objects_All', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"allObj\")\n'])

    for _command in _commands:
        add_command(_command[0], _command[1], _command[2], _command[3], _command[4])