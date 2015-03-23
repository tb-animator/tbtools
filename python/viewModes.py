import maya.cmds as cmds

def viewModes(str):
    '''
    viewModes("joints") to view joints only
	viewModes("meshes") to view meshes only
	viewModes("") to view everything
    '''
    
    
    ver = cmds.about(version=True)
    grease = False
    if ver == "2015" or ver == "2014":
       grease=True

    panel = cmds.getPanel(underPointer=True)
    if not panel:
        panel = cmds.getPanel(withFocus=True)

    if cmds.getPanel(typeOf=panel) == "modelPanel":
        if str == "joints" :
            cmds.modelEditor(panel,edit=True,
                             polymeshes=False,
                             joints=True,
                             nurbsCurves=True,
                             pluginShapes=True,
                             locators=True)
            if grease: cmds.modelEditor(panel,edit=True,greasePencils=False)
        elif str == "meshes":
            cmds.modelEditor(panel,edit=True, 
                             polymeshes=True,
                             strokes=True,
                             joints=False,
                             nurbsCurves=False,
                             pluginShapes=False,
                             locators=False)
            if grease: cmds.modelEditor(panel,edit=True,greasePencils=True)
        else:
            cmds.modelEditor(panel,edit=True, allObjects=True)
            if grease: cmds.modelEditor(panel,edit=True,greasePencils=True)
