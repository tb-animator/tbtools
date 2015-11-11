import maya.cmds as cmds
import tb_messages as message


def viewMode(data):
    """viewModes("joints") to view joints only
    viewModes("meshes") to view meshes only
    viewModes("") to view everything
    """
    ver = cmds.about(version=True)
    grease = ver in {'2014': True, '2015': True}
    panel = cmds.getPanel(underPointer=True) or cmds.getPanel(withFocus=True)

    if cmds.getPanel(typeOf=panel) == "modelPanel":
        if data == "joints":
            state = True
            msg = "controls"
        elif data == "meshes":
            state = False
            msg = "meshes"
        else:
            msg = "controls and meshes"
            message.info(prefix='view', message=' : %s' % msg, position='topLeft')
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

        message.info(prefix='view', message=' : %s' % msg, position='topLeft', fadeStayTime=3.0, fadeOutTime=3.0)
            

