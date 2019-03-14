__author__ = 'Tom'
__author__ = 'tom.bailey'
import maya.cmds as cmds

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import re
import tb_snaps as tb_snaps

reload(tb_snaps)


def ik_toggle(item, mode):
    pm.setAttr(item.ikBlend, mode)
    pm.keyTangent(item.ikBlend, time=[pm.getCurrentTime()],
                  inTangentType="flat",
                  outTangentType="flat")


def ik_match(meta_node=None, mode=False):
    pm.refresh()
    if mode:
        print "ik to fk pose", meta_node
        print pm.listConnections(meta_node.ik_ctrl)[0]
        print pm.listConnections(meta_node.ik_ctrl_snap)[0]
        tb_snaps.orient_snap(pm.listConnections(meta_node.ik_ctrl)[0], pm.listConnections(meta_node.ik_ctrl_snap)[0])
        tb_snaps.variable_point_snap(pm.listConnections(meta_node.ik_ctrl)[0],
                                     pm.listConnections(meta_node.ik_attach_pos)[0],
                                     pm.listConnections(meta_node.ik_pos)[0])
        tb_snaps.point_snap(pm.listConnections(meta_node.pv_ctrl)[0], pm.listConnections(meta_node.pv_ctrl_snap)[0])
    else:
        print "fk to ik pose", meta_node
        tb_snaps.orient_snap(pm.listConnections(meta_node.fk_top)[0], pm.listConnections(meta_node.ik_top)[0])
        tb_snaps.orient_snap(pm.listConnections(meta_node.fk_top)[0], pm.listConnections(meta_node.ik_top)[0])
        tb_snaps.orient_snap(pm.listConnections(meta_node.fk_mid)[0], pm.listConnections(meta_node.ik_mid)[0])
        tb_snaps.orient_snap(pm.listConnections(meta_node.fk_mid)[0], pm.listConnections(meta_node.ik_mid)[0])
        tb_snaps.orient_snap(pm.listConnections(meta_node.fk_end)[0], pm.listConnections(meta_node.ik_end)[0])
        tb_snaps.orient_snap(pm.listConnections(meta_node.fk_end)[0], pm.listConnections(meta_node.ik_end)[0])

'''
Go on have fun figuring this out without the build method
'''
