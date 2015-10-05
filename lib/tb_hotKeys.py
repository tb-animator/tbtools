__author__ = 'tom.bailey'
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


def add_all_commands():
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

    _category = 'AnimTools_selections'
    # up
    _commands.append(['pickwalk_up_replace', 'pickwalks up, replaces selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"up\",\"r\")'])
    _commands.append(['pickwalk_up_add', 'pickwalks up, adds selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"up\",\"a\")'])
    # down
    _commands.append(['pickwalk_down_replace', 'pickwalks down, replaces selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"down\",\"r\")'])
    _commands.append(['pickwalk_down_add', 'pickwalks down, adds selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"down\",\"a\")'])
    # left
    _commands.append(['pickwalk_left_replace', 'pickwalks left, replaces selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"left\",\"r\")'])
    _commands.append(['pickwalk_left_add', 'pickwalks left, adds selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"left\",\"a\")'])
    # right
    _commands.append(['pickwalk_right_replace', 'pickwalks right, replaces selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"right\",\"r\")'])
    _commands.append(['pickwalk_right_add', 'pickwalks right, adds selection', _category, 'python',
                      'import selections as sel\nreload (sel)\nsel.walk(\"right\",\"a\")'])
    # select char nodes
    _commands.append(
        ['select_character_nodes', '', _category, 'python', 'import selections as sel\nreload (sel)\nsel.char()'])
    # isolate toggle
    _commands.append(
        ['isolate_selection', '', _category, 'python', 'import isolate as iso\nreload (iso)\niso.isolate()'])

    _category = 'AnimTools_cameras'

    _commands.append(
        ['tracker_track', 'creates/rebuilds a tracking camera to track your current selection', _category, 'python',
         'import trackingCam as tc\nreload (tc)\ntc.track(\"tracker\")'])
    _commands.append(
        ['tracker_update', 'updates the object tracked by the tracking camera, switches view', _category, 'python',
         'import trackingCam as tc\nreload (tc)\ntc.track(\"newTarget\",\"tracker\")'])
    _commands.append(
        ['tracker_persp', 'swaps the view to the perspective camera, matching your current view', _category, 'python',
         'import trackingCam as tc\nreload (tc)\ntc.track(\"persp\")'])

    _category = 'AnimTools_manipulators'
    _commands.append(['select_ctrls', 'selects all controls for the currently selected character', _category, 'python',
                      'import NT_SelectControls as sc\nreload (sc)\nsc.SelectControls()'])

    _commands.append(['cycle_rotate', 'cycle the rotation mode', _category, 'python',
                      'import manips as mn\nreload (mn)\nmn.cycleRotation()'])
    _commands.append(['cycle_translate', 'cycle the translation mode', _category, 'python',
                      'import manips as mn\nreload (mn)\nmn.cycleTranslation()'])
    _commands.append(
        ['cycle_selection_mask', 'toggle between selecting controls/joints and all objects', _category, 'python',
         'import manips as mn\nreload (mn)\nmn.cycle_selection_mask()'])
    _commands.append(
        ['cycle_key_type', 'cycle between key types, types are set in the options window', _category, 'python',
         'import manips as mn\nreload (mn)\nmn.cycle_key_type()'])

    _commands.append(['smooth_drag_on', 'timeslider tool with no frame snapping', _category, 'python',
                      'import timeDragger as td\nreload (td)\ntd.drag(True)'])
    _commands.append(
        ['smooth_drag_off', 'set this as the release command for whatever you set \'smooth_drag_on\' to', _category,
         'python', 'import timeDragger as td\nreload (td)\ntd.drag(False)'])

    _category = 'AnimTools_view'

    _commands.append(
        ['View_Objects_Joints', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"joints\")'])
    _commands.append(
        ['View_Objects_Meshes', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"meshes\")'])
    _commands.append(
        ['View_Objects_All', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"allObj\")\n'])

    _commands.append(
        ['View_Lighting_None', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"unlit\")\n'])
    _commands.append(
        ['View_Lighting_All', '', _category, 'python', 'import viewMode as vm\nreload (vm)\nvm.viewMode(\"lit\")\n'])
    _commands.append(
        ['view_shaded_lit_textured', '', _category, 'python',
         'import viewMode as vm\nreload (vm)\nvm.viewMode(\"lit\",\"shaded\",\"textured\")\n'])
    _commands.append(['View_Lighting_Default', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"defaultLight\")\n'])
    _commands.append(['View_Lighting_Cycle', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"toggleLight\")\n'])

    _commands.append(['View_Shading_Smooth', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"shaded\")\n'])
    _commands.append(['View_Shading_Wireframe', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"wire\")\n'])
    _commands.append(['View_Shading_Toggle', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"shaded_toggle\")\n'])

    _commands.append(['View_Shading_Wireframe_On_Shaded_On', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"wireOn\")\n'])
    _commands.append(['View_Shading_Wireframe_On_Shaded_Off', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"wireOff\")\n'])
    _commands.append(['View_Shading_Wireframe_On_Shaded_Toggle', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"wireToggle\")\n'])

    _commands.append(['View_Textured_On', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"textured\")\n'])
    _commands.append(['View_Textured_Off', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"untextured\")\n'])
    _commands.append(['View_Textured_Toggle', '', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"toggleTexture\")\n'])

    _commands.append(['View_Xray_On', 'turns xray joints on', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"xray_on\")\n'])
    _commands.append(['View_Xray_Off', 'turns xray joints off', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"xray_off\")\n'])
    _commands.append(['View_Xray_Toggle', 'toggles xray joints', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"xray_toggle\")\n'])

    _commands.append(['renderer_legacy', 'sets rendere to legacy', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"legacy\")\n'])
    _commands.append(['renderer_viewport2', 'sets renderer to viewport 2.0', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"viewport2\")\n'])
    _commands.append(['renderer_toggle', 'toggles viewport renderer', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"toggleRenderer\")\n'])

    _commands.append(['shadows_On', 'turns shadows on', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"shadows\")\n'])
    _commands.append(['shadows_Off', 'turns shadows off', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"noShadows\")\n'])
    _commands.append(['shadows_toggle', 'toggles shadows', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"toggleShadows\")\n'])
    _commands.append(['mesh_toggle_texture', 'toggles textures', _category, 'python',
                      'import viewMode as vm\nreload (vm)\nvm.viewMode(\"toggleTexture\",\"meshes\")\n'])

    _category = 'AnimTools_time'
    _commands.append(['Toggle_play', 'toggle cropping playback', _category, 'python',
                      'import playbackMod as pbm\nreload (pbm)\npbm.playBack("play")\n'])
    _commands.append(['Flip_play', 'play back at every frame', _category, 'python',
                      'import playbackMod as pbm\nreload (pbm)\npbm.playBack("flip")\n'])
    _commands.append(['Timeline_Crop_start', 'toggle cropping playback', _category, 'python',
                      'import playbackMod as pbm\nreload (pbm)\npbm.playBack("crop_start")\n'])
    _commands.append(['Timeline_Crop_end', 'toggle cropping playback', _category, 'python',
                      'import playbackMod as pbm\nreload (pbm)\npbm.playBack("crop_end")\n'])
    _commands.append(['Timeline_Shift_start', 'shifts playback range', _category, 'python',
                      'import playbackMod as pbm\nreload (pbm)\npbm.playBack("shift_start")\n'])
    _commands.append(['Timeline_Shift_end', 'shifts playback range', _category, 'python',
                      'import playbackMod as pbm\nreload (pbm)\npbm.playBack("shift_end")\n'])
    # playblast
    _commands.append(['make_playblast', 'make a helpful playblast', _category, 'python',
                      'import playblasts as plb\nreload (plb)\nplb.make_playblast()\n'])

    _category = 'AnimTools_file'
    _commands.append(['Import_Animations', 'Animation Importer', _category, 'python',
                      'import NT_animationSelector\nreload (NT_animationSelector)\nNT_animationSelector.callMe()\n'])
    _commands.append(['Export_Animations', 'FBX Animation exporter', _category, 'python',
                      'import NT_BatchExporter\nreload(NT_BatchExporter)\nNT_BatchExporter.NT_BatchExporter()\n'])
    _commands.append(
        ['PyAE', 'Generic Python animation import/export', _category, 'python', 'import paie\npaie.GUI() \n'])

    for _command in _commands:
        add_command(_command[0], _command[1], _command[2], _command[3], _command[4])