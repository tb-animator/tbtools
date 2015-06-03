import math
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as om

def track(track,update): 
    _sel = cmds.ls(selection=True)
    _currentView = cmds.lookThru( q=True )
    _cameras = [ 'persp' ] 
    if _sel : 
        sel = _sel[0]

        if cmds.objExists('tracker_grp') :
            _grp = 'tracker_grp'
            _camera = __get_child_camera(_grp)[0]
            
        else :
            print 'rebuilding tracking camera'
            _camera = cmds.camera(name='tracker_cam')
            _grp = cmds.group(empty=True,world=True,name="tracker_grp")
            cmds.parent(_camera,_grp)
        _cameras.append(_camera)
        
        
        if update:
            # constrain group to sel
            _constraint = cmds.listRelatives(_grp,type='parentConstraint')
            if _constraint : cmds.delete(_constraint)
            _constraint = cmds.parentConstraint(_sel,_grp)
            
            # match tracking camera to currentView
        
        copy_view(_cameras[not track],_cameras[track])
        cmds.lookThru(_cameras[track])
    else : print 'error, select something'
    print cmds.lookThru( q=True )
    
def copy_view(_camera,_currentView) :
    print 'matching view from %s to %s'%(_camera,_currentView)
    _xform_T = cmds.xform(_camera,query=True,worldSpace=True,absolute=True,translation=True)
    _xform_R = cmds.xform(_camera,query=True,absolute=True,rotation=True)
    cmds.xform(_currentView,absolute=True,worldSpace=True,translation=_xform_T)
    cmds.xform(_currentView,absolute=True,worldSpace=True,translation=_xform_T)
    cmds.xform(_currentView,absolute=True,rotation=_xform_R)
    

def __get_child_camera(_grp):
    _children = cmds.listRelatives(_grp,children=True,type='transform')
    _cams = []
    for _child in _children : 
        _shape = cmds.listRelatives(_child,shapes=True)
        if cmds.nodeType(_shape) == 'camera' :
            _cams.append(_child)
    return _cams
'''
string $returnSelection[] = `ls -sl`; 

string $objOfInterest[] = `ls -sl`; 
group -empty -name pb_tracking_cam; 
camera -centerOfInterest 5 -focalLength 35 -horizontalFilmAperture 1.4173 -horizontalFilmOffset 0 -verticalFilmAperture 0.9449 -verticalFilmOffset 0 -filmFit Fill -overscan 1 -motionBlur 0 -shutterAngle 144 -nearClipPlane 0.01 -farClipPlane 500 -orthographic 0 -orthographicWidth 30; objectMoveCommand; cameraMakeNode 1 ""; 
rename playblast_cam; 
parent playblast_cam pb_tracking_cam; 
print $objOfInterest[0]; 
parentConstraint -name ($objOfInterest[0]+"_ToPlayblastCam_parentConst") -weight 1 -skipRotate x -sr y -sr z $objOfInterest[0] pb_tracking_cam; 
headsUpMessage "See the world through my eyes";
select $returnSelection;
lookThroughModelPanelClipped playblast_cam modelPanel4 0.001 1000;
fitPanel -selected;
'''

def look(update):
    currentCam = cmds.lookThru( q=True )
    print currentCam
    if update : makeTrackingCam()
