import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

pickwalkName = 'pickwalkInfo'
pickwalkAssetName = 'pickwalk'
pickName = 'pick'
mainName = 'Main'
altName = 'Alt'
conditionAttrName = 'Condition'
conditionName = 'ConditionAttr'
lastName = 'LastIndex'

pickInfoAttrName = 'pickInfo'
destinationListName = 'destination'
altDestinationListName = 'altDestination'
conditionAttributeName = 'ConditionAttribute'
conditionTestValueName = 'ConditionTestValue'
lastUsedIndexName = 'LastUsedIndex'
skipName = 'Skip'
''' Acceptable directions as keys, opposite direction as value'''
directionsDict = {'up': 'down',
                  'upSkip': 'downSkip',
                  'down': 'up',
                  'downSkip': 'upSkip',
                  'left': 'right',
                  'leftSkip': 'rightSkip',
                  'right': 'left',
                  'rightSkip': 'leftSkip'}
walkHotkeyMap = {'up': ['up', False],
                 'upSkip': ['up', True],
                 'down': ['down', False],
                 'downSkip': ['down', True],
                 'left': ['left', False],
                 'leftSkip': ['left', True],
                 'right': ['right', False],
                 'rightSkip': ['right', True]}

walkDirectionNames = {'up': '%s%s' % (pickName, 'Up'),
                      'down': '%s%s' % (pickName, 'Down'),
                      'left': '%s%s' % (pickName, 'Left'),
                      'right': '%s%s' % (pickName, 'Right'),
                      'upSkip': '%s%s%s' % (pickName, skipName, 'Up'),
                      'downSkip': '%s%s%s' % (pickName, skipName, 'Down'),
                      'leftSkip': '%s%s%s' % (pickName, skipName, 'Left'),
                      'rightSkip': '%s%s%s' % (pickName, skipName, 'Right')
                      }

class pickwalkDestinationInfo(object):
    '''
    Node that holds the information for the destination of current pickwalk,
    Build them so they can be stacked to have multiple conditions
    '''

    def __init__(self, name='pick', conditionAttr=None, condition=0.5, destinations=[], altDestinations=[]):
        self.name = name
        self.conditionAttr = conditionAttr
        self.conditionValue = condition
        if not isinstance(destinations, list):
            destinations = [destinations]
        if not isinstance(altDestinations, list):
            altDestinations = [altDestinations]
        self.destinations = destinations
        self.altDestinations = altDestinations
        self.node = None

        self.destinationAttr = None
        self.altDestinationAttr = None
        self.conditionTestValue = None
        self.conditionTestAttribute = None
        self.lastUsedIndexAttr = None

    def create(self):
        '''
        Creates the node that will hold the destination information
        :return:
        '''
        asset = pickwalkAssetName
        if not cmds.objExists(pickwalkAssetName):
            asset = cmds.container(name=pickwalkAssetName,
                                   type='dagContainer',
                                   includeNetworkDetails=("history", "channels"),
                                   includeHierarchyBelow=True,
                                   includeTransform=False,
                                   force=True,
                                   addNode=pickwalkName)
        self.node = cmds.group(name=self.name, empty=True)
        pm.container(asset, edit=True, addNode=self.node)
        cmds.addAttr(self.node, longName=pickInfoAttrName, numberOfChildren=5, attributeType='compound')
        cmds.addAttr(self.node, longName=destinationListName, attributeType='message', parent='pickInfo', multi=True)
        cmds.addAttr(self.node, longName=altDestinationListName, attributeType='message', parent='pickInfo', multi=True)
        cmds.addAttr(self.node, longName=conditionAttributeName, attributeType='message', parent='pickInfo')
        cmds.addAttr(self.node, longName=conditionTestValueName, attributeType='float', parent='pickInfo')
        cmds.addAttr(self.node, longName=lastUsedIndexName, attributeType='long', parent='pickInfo')

        self.destinationAttr = pm.Attribute(self.node + '.' + pickInfoAttrName + '.' + destinationListName)
        self.altDestinationAttr = pm.Attribute(self.node + '.' + pickInfoAttrName + '.' + altDestinationListName)
        if self.conditionAttr:
            self.conditionTestAttribute = pm.Attribute(
                self.node + '.' + pickInfoAttrName + '.' + conditionAttributeName)
            self.conditionTestValue = pm.Attribute(self.node + '.' + pickInfoAttrName + '.' + conditionTestValueName)
        self.lastUsedIndexAttr = pm.Attribute(self.node + '.' + pickInfoAttrName + '.' + lastUsedIndexName)

        if self.destinations:
            print 'destinations', self.destinations
            if isinstance(self.destinations[0], list):
                # got a list of lists,
                self.destinations = self.destinations[0]
            for index, node in enumerate(self.destinations):
                print 'what is node?, ', node
                if node:
                    pm.connectAttr(node + '.message', self.destinationAttr[index], force=True)
        if self.altDestinationAttr:
            for index, node in enumerate(self.altDestinations):
                if not node:
                    return pm.warning('no node for pickwalk')
                pm.connectAttr(node + '.message', self.altDestinationAttr[index], force=True)
        if self.conditionTestAttribute:
            pm.connectAttr(self.conditionAttr, self.conditionTestAttribute, force=True)
        if self.conditionTestValue:
            pm.setAttr(self.conditionTestValue, self.conditionValue)


class pickWalkBuilder(object):
    '''
    Doesn't really need to be a class tbh
    '''

    def __init__(self, node=None):
        self.node = node
        self.target = None
        # self.directionDict = {}

    def addPickwalk(self, direction=None, target=None):
        if direction not in directionsDict.keys():
            return pm.error('bad direction')
        self.target = target
        self.addDirectionAttr(direction)

    def addDirectionAttr(self, direction):
        # add standard direction attribute
        # print walkDirectionNames[direction]
        if not pm.attributeQuery(walkDirectionNames[direction], node=self.node, exists=True):
            # print 'need to add regular attr'
            pm.addAttr(self.node, longName=walkDirectionNames[direction], at='message')
        targetAttribute = pm.Attribute(self.target + '.message')
        pickwalkAttribute = pm.Attribute(self.node + '.' + walkDirectionNames[direction])
        pm.connectAttr(targetAttribute, pickwalkAttribute, force=True)


def addPickwalk(node=None, direction=None, target=None):
    if direction not in directionsDict.keys():
        return pm.error('bad direction')
    # add standard direction attribute
    # print walkDirectionNames[direction]
    if not pm.attributeQuery(walkDirectionNames[direction], node=node, exists=True):
        # print 'need to add regular attr'
        pm.addAttr(node, longName=walkDirectionNames[direction], at='message')
    print 'node', node, 'target', target, 'direction', direction
    if isinstance(target, list):
        if len(target) == 1:
            target = target[0]

    if isinstance(target, list):
        targetAttribute = pm.Attribute(target[0] + '.message')
        pickwalkAttribute = pm.Attribute(node + '.' + walkDirectionNames[direction])
        pm.connectAttr(targetAttribute, pickwalkAttribute, force=True)

    else:
        if target:
            targetAttribute = pm.Attribute(target + '.message')
            pickwalkAttribute = pm.Attribute(node + '.' + walkDirectionNames[direction])
            pm.connectAttr(targetAttribute, pickwalkAttribute, force=True)


def addPickwalkChain(nodes=[],
                     altNodes=[],
                     conditionValue=None,
                     conditionAttribute=None,
                     direction=None,
                     loop=False,
                     reciprocate=True,
                     endOnSelf=False):
    if not nodes:
        return cmds.error('no nodes defined for walk')
    if nodes and altNodes:
        if len(nodes) != len(altNodes):
            return cmds.error('node list lengths do not match')
    if direction not in directionsDict.keys():
        return pm.error('bad direction')
    if not isinstance(nodes, list):
        nodes = [nodes]
    reciprocalIndexes = [None] * len(nodes)
    destinationIndexes = [None] * len(nodes)
    # print destinationIndexes
    # get the corresponding walk indexes
    for index, value in enumerate(nodes):
        # if this is the last index, pick to loop or not
        if index == (len(nodes) - 1):
            if loop:
                # print 'loop', index, (index + 1) % len(nodes)
                destinationIndexes[index] = (index + 1) % len(nodes)

            elif endOnSelf:
                # not looping so set the node to end at this object
                destinationIndexes[index] = index
        else:
            # print 'meh', index, index + 1
            destinationIndexes[index] = index + 1
        # get reciprocal indexes
        if index == 0:
            if loop:
                reciprocalIndexes[index] = len(nodes) - 1
        else:
            reciprocalIndexes[index] = index - 1
    ''' DEBUG '''
    '''
    for index, value in enumerate(destinationIndexes):
        if value is not None:
            print nodes[index], 'walk %s to ' % direction, nodes[value]
    for index, value in enumerate(reciprocalIndexes):
        if value is not None:
            print '\t', index, value
            print nodes[index], 'walk %s to ' % directionsDict[direction], nodes[value]
    '''
    infoNodes = [None] * len(nodes)
    if altNodes:
        for index, value in enumerate(nodes):
            infoNodes[index] = pickwalkDestinationInfo(name='%sInput' % value,
                                                       conditionAttr=pm.Attribute(conditionAttribute),
                                                       condition=conditionValue,
                                                       destinations=nodes[destinationIndexes[index]],
                                                       altDestinations=altNodes[destinationIndexes[index]])
            infoNodes[index].create()
    else:
        for index, value in enumerate(nodes):
            infoNodes[index] = value

    for index, value in enumerate(nodes):
        # get the next index and connect it up to this if reciprocating
        if destinationIndexes[index] is not None:
            addPickwalk(node=value, direction=direction, target=infoNodes[destinationIndexes[index]])
    if reciprocate:
        for index, value in enumerate(reciprocalIndexes):
            if value is not None:
                addPickwalk(node=nodes[index], direction=directionsDict[direction], target=infoNodes[value])


def getInfoNodeDestination(node):
    if not cmds.attributeQuery(pickInfoAttrName, node=node, exists=True):
        # the target doesn't have a pick info attribute, so quit and return the input
        return node
    lastUsedIndex = 0
    destination = None

    # get the index used for picking memory
    if cmds.attributeQuery(lastUsedIndexName, node=node, exists=True):
        lastUsedIndex = cmds.getAttr(node + '.' + pickInfoAttrName + '.' + lastUsedIndexName)
    # first try and get the standard destination, it's ok if it fails
    destination = getAltDestination(lastUsedIndex=lastUsedIndex, node=node)
    if not destination:
        # no alt destination, so look for the standard one
        destination = getStandardDestination(lastUsedIndex=lastUsedIndex, node=node)
    if destination:
        # if the above queries returned anything then send the result to this function again
        return getInfoNodeDestination(destination)
    else:
        # the node did not have any more pick info connections, it's just connected to a node
        # this will probably never trigger in a correct setup
        return node


def getAltDestination(lastUsedIndex=0, node=None):
    destination = None
    if cmds.attributeQuery(altDestinationListName, node=node, exists=True):
        # print '\thas alt destination attr'
        altDestinations = cmds.listConnections(node + '.' + pickInfoAttrName + '.' + altDestinationListName)
        if altDestinations:
            # print 'has valid alt destination list'
            # print altDestinations
            # has alt destinations, check for test attribute
            if cmds.attributeQuery(conditionAttributeName, node=node, exists=True):
                conditionPlugs = cmds.listConnections(node + '.' + pickInfoAttrName + '.' + conditionAttributeName,
                                                      plugs=True)
                if conditionPlugs:
                    conditionCurrentValue = cmds.getAttr(conditionPlugs[0])

                if cmds.attributeQuery(conditionTestValueName, node=node, exists=True):
                    # print 'checking test value'
                    conditionTestValue = cmds.getAttr(node + '.' + conditionTestValueName)
                    if conditionCurrentValue >= conditionTestValue:
                        ''' PICK ALT DESTINATION '''
                        # print 'PICK ALT DESTINATION'
                        if lastUsedIndex <= len(altDestinations):
                            destination = altDestinations[lastUsedIndex]
                        else:
                            destination = altDestinations[0]
                else:
                    pm.warning('no %s attribute on pick walk node %s' % (conditionTestValueName, node))
            else:
                pm.warning('no %s attribute on pick walk node %s' % (conditionAttributeName, node))
    else:
        print 'no valid alt destinations attribute'
    return destination


def getStandardDestination(lastUsedIndex=0, node=None):
    # didnt get a destination from the alternate check, default to regular path
    if cmds.attributeQuery(destinationListName, node=node, exists=True):
        destinationConnections = cmds.listConnections(node + '.' + pickInfoAttrName + '.' + destinationListName)
        # if we have a destination list, check the index uses last
        if destinationConnections:
            if lastUsedIndex <= len(destinationListName):
                destination = destinationConnections[lastUsedIndex]
            else:
                destination = destinationConnections[0]
    return destination


def pickWalk(node=None, direction=None, add=False):
    # check for valid direction
    if direction not in directionsDict.keys():
        return cmds.error('\nInvalid pick direction, only up, down, left, right are supported')
    # check if message attribute exists
    if not cmds.attributeQuery(walkDirectionNames[direction], node=node, exists=True):
        pass
    # list connection to message attribute
    conns = cmds.listConnections(node + '.' + walkDirectionNames[direction], source=True, destination=False)

    if conns:
        destinationNode = getInfoNodeDestination(conns[0])
        if destinationNode:
            updateLastIndex(node=node)
            return destinationNode
    else:
        pickwalkStandard().walk(direction=direction)

class pickwalkStandard:
    """
    holds the failsafe default maya commands
    """
    directionsDict = {'up': 'pickWalkUp',
                      'upSkip': 'pickWalkUp',
                      'down': 'pickWalkDown',
                      'downSkip': 'pickWalkDown',
                      'left': 'pickWalkRight',
                      'leftSkip': 'pickWalkRight',
                      'right': 'pickWalkLeft',
                      'rightSkip': 'pickWalkLeft'}

    def walk(self, direction):
        mel.eval(self.directionsDict[direction])


def getRigInfoPickWalk(node=None, direction=None):
    returnedConnections = []

    if direction not in directionsDict.keys():
        return cmds.error('\nInvalid pick direction, only up, down, left, right are supported')
    # check if message attribute exists
    if not cmds.attributeQuery(walkDirectionNames[direction], node=node, exists=True):
        return
    conns = cmds.listConnections(node + '.' + walkDirectionNames[direction], source=True, destination=False)
    if conns:
        for c in conns:
            returnedConnections.extend(getRigDestination(c))
    if not returnedConnections:
        return conns
    return returnedConnections


def getRigInfoPickWalkAttributes(node=None):
    existingAttrs = []
    for attr in walkDirectionNames.values():
        # print attr
        if pm.attributeQuery(attr, node=node, exists=True):
            existingAttrs.append(attr)
    return existingAttrs


def getRigDestination(node=None):
    # didnt get a destination from the alternate check, default to regular path
    if cmds.attributeQuery(destinationListName, node=node, exists=True):
        destinationConnections = cmds.listConnections(node + '.' + pickInfoAttrName + '.' + destinationListName)
        # if we have a destination list, check the index uses last
        if destinationConnections:
            return destinationConnections
    return []


def updateLastIndex(node=None):
    conns = cmds.listConnections(node + '.message', type='transform')
    if conns:
        for con in conns:
            # check if the connection has a pickwalk attribute
            if cmds.attributeQuery(pickInfoAttrName, node=con, exists=True):
                newIndex = getIndexOfConnection(con, pickInfoAttrName + '.' + destinationListName, node)
                if newIndex is None:
                    newIndex = getIndexOfConnection(con, pickInfoAttrName + '.' + altDestinationListName, node)

                if newIndex is not None:
                    if cmds.attributeQuery(lastUsedIndexName, node=con, exists=True):
                        cmds.setAttr(con + '.' + pickInfoAttrName + '.' + lastUsedIndexName, newIndex)


def getIndexOfConnection(node, attribute, target):
    conns = cmds.listConnections(node + '.' + attribute)
    if conns:
        if target in conns:
            return conns.index(target)
    else:
        return None


class pickwalker():
    def __init__(self):
        '''
        all the direction named attributes I've seen used so far
        '''
        self.picwalkAttributeNames = {'up': [walkDirectionNames['up'],
                                             '_pickwalk_up',
                                             'cgTkPickWalkup',
                                             'zooWalkup'],
                                      'down': [walkDirectionNames['down'],
                                               '_pickwalk_down',
                                               'cgTkPickWalkdown',
                                               'zooWalkdown'],
                                      'left': [walkDirectionNames['left'],
                                               '_pickwalk_left',
                                               'cgTkPickWalkleft',
                                               'zookWalkleft'],
                                      'right': [walkDirectionNames['right'],
                                                '_pickwalk_right',
                                                'cgTkPickWalkright',
                                                'zookWalkright'],
                                      'upSkip': [walkDirectionNames['upSkip'],
                                                 walkDirectionNames['up'],
                                                 '_pickwalk_up',
                                                 'cgTkPickWalkup',
                                                 'zooWalkup'],
                                      'downSkip': [walkDirectionNames['downSkip'],
                                                   walkDirectionNames['down'],
                                                   '_pickwalk_down',
                                                   'cgTkPickWalkdown',
                                                   'zooWalkdown'],
                                      'leftSkip': [walkDirectionNames['leftSkip'],
                                                   walkDirectionNames['left'],
                                                   '_pickwalk_left',
                                                   'cgTkPickWalkleft',
                                                   'zookWalkleft'],
                                      'rightSkip': [walkDirectionNames['rightSkip'],
                                                    walkDirectionNames['right'],
                                                    '_pickwalk_right',
                                                    'cgTkPickWalkright',
                                                    'zookWalkright'],

                                      }
        self.melCommands = {'up': 'pickWalkUp',
                            'down': 'pickWalkDown',
                            'left': 'pickWalkLeft',
                            'right': 'pickWalkRight',
                            'upSkip': 'pickWalkUp',
                            'downSkip': 'pickWalkDown',
                            'leftSkip': 'pickWalkLeft',
                            'rightSkip': 'pickWalkRight'
                            }

    def walk(self, direction='up', add=False):
        print 'walking, add =', add
        self.selection = cmds.ls(sl=True)
        self.returnedControls = []
        if not self.selection:
            return cmds.warning('\nNothing selected to pickwalk')
        if direction not in directionsDict.keys():
            return cmds.error('\nInvalid pick direction, only up, down, left, right are supported')
        # do a quick check for any custom pickwalk attributes, if there are none,
        # then just bail and do regular pickwalking
        userAttrs = cmds.listAttr(self.selection, userDefined=True)
        if not userAttrs:
            mel.eval(self.melCommands[direction])
            return
        pickAttributes = [i for i in self.picwalkAttributeNames[direction] if i in userAttrs]
        if not pickAttributes:
            # didn't find any custom pickwalk attributes, use the regular walk
            mel.eval(self.melCommands[direction])
            return
        for s in self.selection:
            found = False
            for walkAttribute in self.picwalkAttributeNames[direction]:
                if not found:
                    if cmds.attributeQuery(walkAttribute, node=s, exists=True):
                        returnObj = self.pickWalk(node=s, attribute=walkAttribute)
                        if returnObj:
                            if isinstance(returnObj, list):
                                self.returnedControls.extend(returnObj)
                                found = True
                            else:
                                self.returnedControls.append(returnObj)
                                found = True

        if add:
            print 'adding'
            self.returnedControls.extend(self.selection)
        cmds.select(self.returnedControls, replace=True)

    def pickWalk(self, node=None, attribute=None):
        # check if message attribute exists
        if not cmds.attributeQuery(attribute, node=node, exists=True):
            return
        # walk attribute exists, check it's type
        if cmds.getAttr(node + '.' + attribute, type=True) == u'string':
            # use string attribute method
            destination = cmds.getAttr(node + '.' + attribute)
            pNode = pm.PyNode(node)
            if cmds.objExists(pNode.namespace() + cmds.getAttr(node + '.' + attribute)):
                return pNode.namespace() + destination

        elif cmds.getAttr(node + '.' + attribute, type=True) == u'message':
            # list connection to message attribute
            conns = cmds.listConnections(node + '.' + attribute, source=True, destination=False)
            # if there are connections, check what kind of node it is
            if conns:
                destinationNode = getInfoNodeDestination(conns[0])
                if destinationNode:
                    updateLastIndex(node=node)
                    return destinationNode


class tb_hkey:
    """
    class for holding hotkey command info
    """

    def __init__(self, name="", annotation="", category="tb_tools", language='python', command=[""]):
        self.name = name
        self.annotation = annotation
        self.category = category
        self.language = language
        self.runTimeCommand = None
        self.command = self.collapse_command_list(command)

        self.add()

    def collapse_command_list(self, command):
        cmd = ""
        for lines in command:
            cmd = cmd + lines + "\n"
        return cmd

    def add(self):
        if not cmds.runTimeCommand(self.name, exists=True):
            cmds.runTimeCommand(self.name)
        self.runTimeCommand = cmds.runTimeCommand(self.name,
                                                  edit=True,
                                                  annotation=self.annotation,
                                                  category=self.category,
                                                  commandLanguage=self.language,
                                                  command=self.command)
        cmds.nameCommand(self.name + 'NameCommand',
                         annotation=self.name + 'NameCommand',
                         command=self.name,
                         sourceType='mel')
        self.hotkeyName = self.name + 'NameCommand'


def create_pickwalk_hotkeys():
    category = 'tbtools_selection'
    for key in directionsDict.keys():
        command = tb_hkey(name='tb_%s' % walkDirectionNames[key],
                          annotation='smart pickwalker',
                          category=category,
                          command=['global walker',
                                   'try:',
                                   '	walker.walk(direction="%s", add=False)' % key,
                                   'except:',
                                   '	from tb_pickWalker import pickwalker',
                                   '	walker = pickwalker()',
                                   '	walker.walk(direction="%s", add=False)' % key])
        command_add = tb_hkey(name='tb_%s_add' % walkDirectionNames[key],
                              annotation='smart pickwalker',
                              category=category,
                              command=['global walker',
                                       'try:',
                                       '	walker.walk(direction="%s", add=True)' % key,
                                       'except:',
                                       '	from tb_pickWalker import pickwalker',
                                       '	walker = pickwalker()',
                                       '	walker.walk(direction="%s", add=True)' % key])

        cmds.hotkey(keyShortcut=walkHotkeyMap[key][0],
                    ctrlModifier=walkHotkeyMap[key][1],
                    name=command.hotkeyName)
        cmds.hotkey(keyShortcut=walkHotkeyMap[key][0],
                    shiftModifier=True,
                    ctrlModifier=walkHotkeyMap[key][1],
                    name=command_add.hotkeyName)
    cmds.savePrefs(hotkeys=True)


def collapse_command_list(command):
    '''
    Collapses a list of strings into one string
    :param command:
    :return:
    '''
    cmd = ""
    for lines in command:
        cmd = cmd + lines + "\n"
    return cmd
