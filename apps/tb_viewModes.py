import maya.cmds as cmds
import pymel.core as pm
import tb_messages as message
from tb_objectInfo import mod_panel


def viewMode(data):
    """viewModes("joints") to view joints only
    viewModes("meshes") to view meshes only
    viewModes("") to view everything
    """
    # should organise these nicer
    show_message = pm.optionVar.get('tb_viewmode_msg', False)
    message_pos = pm.optionVar.get('tb_viewmode_msg_pos', 'topLeft')

    ver = cmds.about(version=True)
    grease = ver in {'2014': True, '2015': True}
    panel = mod_panel().getModelPanel()

    if cmds.getPanel(typeOf=panel) == "modelPanel":
        if data == "joints":
            state = True
            msg = "controls"
        elif data == "meshes":
            state = False
            msg = "meshes"
        else:
            msg = "controls and meshes"
            if show_message:
                message.info(prefix='view',
                             message=' : %s' % msg,
                             position=message_pos,
                             fadeStayTime=3.0,
                             fadeOutTime=3.0)
            cmds.modelEditor(panel, edit=True, allObjects=True)
            return

        cmds.modelEditor(panel, edit=True, 
                         polymeshes=not state,
                         strokes=not state,
                         joints=state,
                         nurbsCurves=state,
                         pluginShapes=state,
                         locators=state)
        if grease: 
            cmds.modelEditor(panel, edit=True, greasePencils=True)
        if show_message:
            message.info(prefix='view',
                         message=' : %s' % msg,
                         position=message_pos,
                         fadeStayTime=3.0,
                         fadeOutTime=3.0)
            

