__author__ = 'tom.bailey'
import pymel.core as pm
import pymel.core.datatypes as dt

import re
import rig.parent_tools as pt
reload(pt)

def orient_snap(source, target):
    pm.xform(source,
             absolute=True,
             worldSpace=True,
             rotation=pm.xform(target,
                               query=True,
                               absolute=True,
                               worldSpace=True,
                               rotation=True))


def point_snap(source, target):
    """
    works with odd frozen translate objects by measuring things
    """
    source_pivot = dt.Vector(pm.xform(source, query=True, worldSpace=True, rotatePivot=True))
    target_pivot = dt.Vector(pm.xform(target, query=True, worldSpace=True, rotatePivot=True))

    source_ws = dt.Vector(pm.xform(source, query=True, worldSpace=True, translation=True))

    _position_difference = target_pivot - source_pivot
    _position_result = source_ws + _position_difference

    pm.xform(source, absolute=True, worldSpace=True, translation=_position_result)

def variable_point_snap(source, snapObject, target):
    """
    works with odd frozen translate objects by measuring things
    """
    print "variable snap", source, snapObject, target
    source_pivot = dt.Vector(pm.xform(source, query=True, worldSpace=True, rotatePivot=True))
    snap_pivot = dt.Vector(pm.xform(source, query=True, worldSpace=True, translation=True))
    target_pivot = dt.Vector(pm.xform(target, query=True, worldSpace=True, translation=True))

    source_ws = dt.Vector(pm.xform(source, query=True, absolute=True, worldSpace=True, translation=True))

    _position_difference = target_pivot - snap_pivot
    print snap_pivot, "\n", target_pivot, "\n", _position_difference
    _position_result = source_ws + _position_difference

    pm.xform(source, absolute=True, worldSpace=True, translation=_position_result)


class SnapTools():
    def __init__(self):
        pass

    def snap_selection(self):
        sel = pm.ls(selection=True)
        if len(sel) >= 2:
            original = sel[0]
            target = sel[1]

            original_rotation = xforms().get_world_rotation(original)
            original_pivot_position = xforms().get_world_pivot(original)
            original_world_position = xforms().get_world_space(original)

            target_rotation = xforms().get_world_rotation(target)
            target_pivot_position = xforms().get_world_pivot(target)
            target_world_position = xforms().get_world_space(target)

            _pivot_difference = vector_tools().minus(target_pivot_position, original_pivot_position)
            _out_position = vector_tools().plus(original_world_position, _pivot_difference)

            xforms.set_world_space(original, _out_position)
            xforms.set_world_rotation(original, target_rotation)
            xforms.set_world_rotation(original, target_rotation)

            #orient_snap(original, target)


            rot = pm.xform(target, query=True, absolute=True, worldSpace=True, rotation=True)
            node_ro = pm.xform(original, query=True, rotateOrder=True)
            ro = pm.xform(target, query=True, rotateOrder=True)
            pm.xform(original, absolute=True, worldSpace=True, rotation=rot, rotateOrder=ro, preserve=True)
            pm.xform(original, rotateOrder=node_ro, preserve=True)

    @staticmethod
    def store_transform():
        sel = pm.ls(selection=True)
        if sel:
            _position = xforms().get_world_space(sel[0])
            _rotation = xforms().get_world_rotation(sel[0])
            pm.optionVar(floatValue=('NT_xform_Pos_1', _position[0]))
            pm.optionVar(floatValueAppend=('NT_xform_Pos_1', _position[1]))
            pm.optionVar(floatValueAppend=('NT_xform_Pos_1', _position[2]))

            pm.optionVar(floatValue=('NT_xform_Rot_1', _rotation[0]))
            pm.optionVar(floatValueAppend=('NT_xform_Rot_1', _rotation[1]))
            pm.optionVar(floatValueAppend=('NT_xform_Rot_1', _rotation[2]))

            print pm.optionVar['NT_xform_Pos_1']
            print pm.optionVar['NT_xform_Rot_1']
        pass

    def restore_transform(self):
        sel = pm.ls(selection=True)
        if sel:
            _position = pm.optionVar['NT_xform_Pos_1']
            _rotation = pm.optionVar['NT_xform_Rot_1']
            xforms().set_world_space(sel[0], _position)
            xforms().set_world_rotation(sel[0], _rotation)
        pass

class xforms():
    def __init__(self):
        pass

    @staticmethod
    def get_world_pivot(node):
        # get the world pivot
        return pm.xform(node, query=True, worldSpace=True, rotatePivot=True)

    @staticmethod
    def get_world_space(node):
        # gets the world space, not really world space tho, just what maya thinks is world space
        return pm.xform(node, query=True, relative=True, worldSpace=True, translation=True)

    @staticmethod
    def set_world_space(node, position):
        # set the world space position on the object
        pm.xform(node, absolute=True, worldSpace=True, translation=position)

    @staticmethod
    def get_world_rotation(node):
        # get the absolute world rotation of the object
        return pm.xform(node, query=True, absolute=True, worldSpace=True, rotation=True)

    @staticmethod
    def set_world_rotation(node, rotation):
        # set the absolute world rotation
        pm.xform(node, absolute=True, worldSpace=True, rotation=rotation)

class vector_tools():
    @staticmethod
    def minus(vector1, vector2):
        return [vector1[0] - vector2[0], vector1[1] - vector2[1], vector1[2] - vector2[2]]

    @staticmethod
    def plus(vector1, vector2):
        return [vector1[0] + vector2[0], vector1[1] + vector2[1], vector1[2] + vector2[2]]

def snap_pivots(meta_node, snapNode, extraKey=False, reverse=False):
    ctrlNode = pm.listConnections(meta_node.control)[0]
    attachNode = pm.listConnections(meta_node.attach_pivot)[0]
    pivotNode = pm.listConnections(meta_node.animate_pivot)[0]

    # cache auto key state and turn it off
    keyState = pm.autoKeyframe(query=True,  state=True)
    pm.autoKeyframe(state=False)

    # query the tangents
    #_in = pm.keyTangent(g=True, query=True, inTangentType=True)[0]
    #_out = pm.keyTangent(g=True, query=True, outTangentType=True)[0]
    '''
    pm.setKeyframe(ctrlNode,
                   time=pm.getCurrentTime() -1,
                   insert=True,
                   attribute=['translate', 'rotate'])
    '''
    if extraKey:
        pm.setKeyframe(ctrlNode,
                   time=[pm.getCurrentTime()-1],
                   inTangentType='linear',
                   outTangentType='linear',
                   attribute=['translate', 'rotate', 'AnimPivot'])
    pm.setKeyframe(ctrlNode,
                   time=[pm.getCurrentTime()],
                   inTangentType='linear',
                   outTangentType='linear',
                   attribute=['translate', 'rotate', 'AnimPivot'])
    # get our current control location (so we know how much to adjust it by after moving the pivot
    ctrlPos = dt.Vector(pm.xform(ctrlNode, query=True, worldSpace=False,translation=True))
    pivotPos = dt.Vector(pm.xform(pivotNode, query=True, worldSpace=True,translation=True))
    # get the new pivot location
    snapXform = pm.xform(snapNode, query=True, worldSpace=False,translation=True)
    #

    pre_attachXform = dt.Vector(pm.xform(attachNode, query=True, worldSpace=True,translation=True))
    # move the pivot attribute
    # pm.xform(pivotNode, worldSpace=False, translation=snapXform)
    ctrlNode.AnimPivot.set(snapXform)
    post_attachXform = dt.Vector(pm.xform(attachNode, query=True, worldSpace=True,translation=True))
    post_pivotXform = dt.Vector(pm.xform(pivotNode, query=True, worldSpace=True,translation=True))
    if not reverse:
        pm.xform(ctrlNode, worldSpace=False, translation=pre_attachXform - post_attachXform + ctrlPos)
    else:
        pm.xform(ctrlNode, worldSpace=False, translation=pivotPos - post_pivotXform + ctrlPos)
        pass
    # pm.setKeyframe(pivotNode, inTangentType='linear', outTangentType='step')

    pm.setKeyframe(ctrlNode, inTangentType='linear', outTangentType='linear', attribute=['translate', 'rotate', 'AnimPivot'])

    # restore autokey state
    pm.autoKeyframe(state=keyState)
    pm.refresh()

if not pm.optionVar(exists='NT_xform_Pos_1'):
    pm.optionVar(floatValue=('NT_xform_Pos_1', 0.0))
    pm.optionVar(floatValueAppend=('NT_xform_Pos_1', 0.0))
    pm.optionVar(floatValueAppend=('NT_xform_Pos_1', 0.0))
if not pm.optionVar(exists='NT_xform_Rot_1'):
    pm.optionVar(floatValue=('NT_xform_Rot_1', 0.0))
    pm.optionVar(floatValueAppend=('NT_xform_Rot_1', 0.0))
    pm.optionVar(floatValueAppend=('NT_xform_Rot_1', 0.0))