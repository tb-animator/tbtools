import pymel.core as pm
from tb_objectInfo import Attributes

__author__ = 'Tom'
# pickwalk data object
class pickInfo():
    def __init__(self, control="", up="", down="", left="", right=""):
        self.control = control
        self.up = up
        self.down = down
        self.left = left
        self.right = right


def get_sides(side=""):
    sides = {"left": ["l_", "r_"], "right": ["r_", "l_"]}
    return sides.get(side, "")


def setup_pickwalking(pickList=[]):
    for picks in pickList:
        if picks.up:
            Attributes().connect_message(source=picks.control,
                                         destination=pm.PyNode(picks.up),
                                         attribute='cgTkPickWalkup')
        if picks.down:
            Attributes().connect_message(source=picks.control,
                                         destination=pm.PyNode(picks.down),
                                         attribute='cgTkPickWalkdown')
        if picks.left:
            Attributes().connect_message(source=picks.control,
                                         destination=pm.PyNode(picks.left),
                                         attribute='cgTkPickWalkleft')
        if picks.right:
            Attributes().connect_message(source=picks.control,
                                         destination=pm.PyNode(picks.right),
                                         attribute='cgTkPickWalkright')