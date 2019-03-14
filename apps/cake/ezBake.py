from tb_isolator import isolator
import pymel.core as pm
import maya.cmds as cmds
from tb_timeline import timeline

class bakeToLayer():
    def __init__(self):
        self.sel = cmds.ls(selection=True)
        self.objs = dict()

        print self.sel

        for s in self.sel: self.objs[s] = self.makeLocator(s)

        isolator().isolateAll(state=True)


        isolator().isolateAll(state=False)

    def makeLocator(self, obj):
        loc = cmds.spaceLocator(name='%s_BAKED_' % obj)[0]
        cmds.parentConstraint(obj, loc, maintainOffset=False)
        return loc

    def bake(self):
        print 'Baking', self.objs

        # bake the keys down on the new layer
        cmds.bakeResults(list(self.objs.values()), simulation=False,
                         disableImplicitControl=False,
                         #removeBakedAttributeFromLayer=False,
                         #destinationLayer=resultLayer,
                         #bakeOnOverrideLayer=False,
                         time=(0, 100),
                         sampleBy=1)

        pass

    def unBake(self):
        pass


def bake_to_override():
    sel = pm.ls(sl=True)
    preBakeLayers = pm.ls(type='animLayer')
    pm.bakeResults(sel,
                     time=(timeline().get_smart_range()[0], timeline().get_smart_range()[1]),
                     simulation=True,
                     sampleBy=1,
                     oversamplingRate=1,
                     disableImplicitControl=True,
                     preserveOutsideKeys=False,
                     sparseAnimCurveBake=True,
                     removeBakedAttributeFromLayer=False,
                     removeBakedAnimFromLayer=False,
                     bakeOnOverrideLayer=True,
                     minimizeRotation=True,
                     controlPoints=False,
                     shape=False)
    postBakeLayer = [x for x in pm.ls(type='animLayer') if x not in preBakeLayers]
    for newAnimLayer in postBakeLayer:
        pm.setAttr(newAnimLayer + ".ghostColor", 16)
        pm.rename(newAnimLayer, sel[0].namespace()[:-1] + '_' + sel[0].stripNamespace() + '_baked')

def bake_to_locator(constrain=False, orientOnly=False):
    sel = pm.ls(sl=True)
    locs = []
    constraints = []
    if sel:
        for s in sel:
            loc = pm.spaceLocator(name=s + '_baked')
            print loc
            loc.localScale.set(10,10,10)
            loc.getShape().overrideEnabled.set(True)
            loc.getShape().overrideColor.set(14)
            const = pm.parentConstraint(s, loc)
            locs.append(loc)
            constraints.append(const)
    if locs:
        pm.bakeResults(locs,
                       simulation=False,
                       disableImplicitControl=False,
                       time=[pm.playbackOptions(query=True, minTime=True), pm.playbackOptions(query=True, maxTime=True)],
                       sampleBy=1)
        if constrain:
            pm.delete(constraints)
            for cnt, loc in zip(sel, locs):
                skipT, skipR = get_available_attrs(cnt)
                pm.parentConstraint(loc, cnt, skipTranslate={True: ('x','y','z'), False:skipT}[orientOnly], skipRotate=skipR)

def get_available_attrs(node):
    '''
    returns 2 lists of attrs that are not available for constraining
    '''
    attrs = ['X', 'Y', 'Z']

    lockedTranslates = []
    lockedRotates = []
    for attr in attrs:
        if not pm.getAttr(node + '.' + 'translate' + attr, settable=True):
            lockedTranslates.append(attr.lower())
        if not pm.getAttr(node + '.' + 'rotate' + attr, settable=True):
            lockedRotates.append(attr.lower())

    return lockedTranslates, lockedRotates

class get_available_attributes(object):
    def __init__(self, node, mode=''):
        '''
        returns attrs that are not available for constraining
        '''
        self.result = [attr.lower() for attr in ['X', 'Y', 'Z'] if not pm.getAttr(node + '.' + mode + attr, settable=True)]

class get_available_translates(get_available_attributes):
    def __init__(self, node):
        super(get_available_translates, self).__init__(node, mode='translate')

class get_available_rotates(get_available_attributes):
    def __init__(self, node):
        super(get_available_rotates, self).__init__(node, mode='rotate')

class get_available_scales(get_available_attributes):
    def __init__(self, node):
        super(get_available_scales, self).__init__(node, mode='scale')

def parentConst(constrainGroup=False, offset=True, postBake=False, postReverseConst=False):
    drivers = pm.ls(sl=True)
    if not len(drivers) > 1:
        return pm.warning('not enough objects selected to constrain, please select at least 2')
    target = drivers.pop(-1)

    if constrainGroup:
        if not target.getParent():
            pm.warning("trying to constrain object's parent, but it is parented to the world")
        else:
            target = target.getParent()
    pm.parentConstraint(drivers, target,
                        skipTranslate=get_available_translates(target).result,
                        skipRotate=get_available_rotates(target).result,
                        maintainOffset=offset)
    if postBake:
        quickBake(target)
        if postReverseConst:
            if len(drivers) != 1:
                return pm.warning('Can only post reverse constraint if 2 objects are used')
            else:
                pm.parentConstraint(target, drivers[0],
                                    skipTranslate=get_available_translates(drivers[0]).result,
                                    skipRotate=get_available_rotates(drivers[0]).result,
                                    maintainOffset=True)

def clearBlendAttrs(node):
    for attr in pm.listAttr(node):
        if 'blendParent' in str(attr):
            pm.deleteAttr(node, at=attr)

def quickBake(node):
    pm.bakeResults(node,
                   simulation=False,
                   disableImplicitControl=False,
                   time=[pm.playbackOptions(query=True, minTime=True), pm.playbackOptions(query=True, maxTime=True)],
                   sampleBy=1)

    pm.delete(node.listRelatives(type='constraint'))
    clearBlendAttrs(node)