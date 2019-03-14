import pymel.core as pm
import pymel.core.datatypes as dt

sides = {'l_': 'r_', 'r_': 'l_'}

class coneReader():
    def __init__(self, driver=None, parent=None, axis='y', flip=False):
        self.driver = driver
        self.parent = parent
        self.downAxis = axis
        self.flip = flip
        self.pose_group = None
        self.poseMarkers = {}
        self.poseRemaps = {}
        self.poseOffsets = {}

    def __setattr__(self, name, value):
        if name == 'driver':
            print 'checking driver'
            self.set_driver(value)
        elif name == 'parent':
            print 'checking parent'
            self.set_parent(value)
        else:
            print 'default'
            self.__dict__[name] = value

    def set_parent(self, value):
        if value:
            if pm.objExists(value):
                self.__dict__['parent'] = value
        else:
            self.__dict__['parent'] = None

    def set_driver(self, value):
        if value:
            if pm.objExists(value):
                self.__dict__['driver'] = value
        else:
            self.__dict__['driver'] = None

    def add_rest_locator(self):
        currentRot = pm.getAttr(self.driver + '.rotate')
        pm.setAttr(self.driver + '.rotate', [0,0,0])
        self.add_pose_locator(name='rest')
        pm.parentConstraint(self.driver, self.poseMarkers['rest'], maintainOffset=True)

        # restore current pose
        pm.setAttr(self.driver + '.rotate', currentRot)

    def add_pose_locator(self, name='rest'):
        if self.pose_group:
            if pm.objExists(self.driver + '_' + name + '_pose'):
                self.poseMarkers[name] = self.driver + '_' + name + '_pose'
            else:
                self.poseMarkers[name] = cmds.spaceLocator(name=self.driver + '_' + name + '_pose')[0]
                # parent new locator to driver
            pm.parent(self.poseMarkers[name], self.driver)
            pm.setAttr(self.poseMarkers[name] + '.translate', [0,0,0])
            pm.setAttr(self.poseMarkers[name] + '.t%s' % self.downAxis, {True: -1, False: 1}[self.flip])

            # parent new locator to main group
            pm.parent(self.poseMarkers[name], self.pose_group)
            self.poseOffsets[name] = pm.getAttr(self.poseMarkers[name] + '.translate')

    def create_pose(self, name='rest'):
        self.add_pose_locator(name=name)
        # vectorProduct
        dotProduct = pm.createNode('vectorProduct', name=self.driver + '_' + name + '_dotProduct')
        dotProduct.normalizeOutput.set(1)
        pm.connectAttr(self.poseMarkers['rest']+'.translate', dotProduct.input1)
        pm.connectAttr(self.poseMarkers[name]+'.translate', dotProduct.input2)
        self.poseRemaps[name] = pm.createNode('remapValue', name=self.driver + '_' + name + '_remap')
        pm.setAttr(self.poseRemaps[name]+'.value[0].value_Interp', 2)
        pm.setAttr(self.poseRemaps[name]+'.value[1].value_Interp', 0)
        pm.connectAttr(dotProduct.outputX, self.poseRemaps[name]+'.inputValue')

        if not pm.attributeQuery('pose_'+name, node=self.driver, exists=True):
            pm.addAttr(self.driver, ln='pose_'+name, at='float', keyable=True)

        pm.connectAttr(self.poseRemaps[name]+'.outValue', self.driver+'.pose_'+name, force=True)

    def set_rest_position(self):
        currentRot = pm.getAttr(self.driver + '.rotate')

        # set the rotation to rest pose
        pm.setAttr(self.driver + '.rotate', [0,0,0])

        for remap in self.poseRemaps:
            # set new default 0 pose on remap
            pm.setAttr(self.poseRemaps[remap] + '.inputMin', pm.getAttr(self.poseRemaps[remap] + '.inputValue'))

        # reset the rotation to original
        pm.setAttr(self.driver + '.rotate', currentRot)

    def add_pose_group(self):
        if pm.objExists(self.driver + '_pose_grp'):
            self.pose_group = self.driver + '_pose_grp'
            print 'found existing pose group, using', self.driver + '_pose_grp'
        else:
            self.pose_group = cmds.group(empty=True, name=self.driver + '_pose_grp')
            pm.delete(pm.pointConstraint(self.parent, self.pose_group))
            pm.delete(pm.pointConstraint(self.driver, self.pose_group))
            pm.parentConstraint(self.parent, self.pose_group, maintainOffset=True)

        self.add_rest_locator()

    def find_opposite(self):
        for key in sides.keys():
            if self.parent.startswith(key):
                if pm.objExists(self.parent.replace(key, sides[key])):
                    print 'found opposite side', self.parent.replace(key, sides[key])

    def build(self):
        pass


class coneReaderUI():
    def __init__(self):
        self.coneReader = coneReader()
        self.window = pm.window(title='cone reader')

    def showUI(self):
        self.window.show()

'''
I honestly can't remember what this is, it's probably in the rig builder somewhere
crWindow = coneReaderUI()
crWindow.showUI()

cReader = coneReader(axis='x', flip=True)
cReader.parent = 'l_shoulder'
cReader.driver = 'l_arm'
cReader.find_opposite()
cReader.add_pose_group()
cReader.create_pose(name='fwd')
cReader.set_rest_position()
#cReader.poseOffsets
'''