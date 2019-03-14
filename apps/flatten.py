import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import math
import sys
import pymel.core as pm
import pymel.core.datatypes as dt


def getMatrix(node):
    '''
    Gets the world matrix of an object based on name.
    '''
    #Selection list object and MObject for our matrix
    selection = OpenMaya.MSelectionList()
    matrixObject = OpenMaya.MObject()

    #Adding object
    selection.add(node)

    #New api is nice since it will just return an MObject instead of taking two arguments.
    MObjectA = selection.getDependNode(0)

    #Dependency node so we can get the worldMatrix attribute
    fnThisNode = OpenMaya.MFnDependencyNode(MObjectA)

    #Get it's world matrix plug
    worldMatrixAttr = fnThisNode.attribute( "worldMatrix" )

    #Getting mPlug by plugging in our MObject and attribute
    matrixPlug = OpenMaya.MPlug( MObjectA, worldMatrixAttr )
    matrixPlug = matrixPlug.elementByLogicalIndex( 0 )

    #Get matrix plug as MObject so we can get it's data.
    matrixObject = matrixPlug.asMObject(  )

    #Finally get the data
    worldMatrixData = OpenMaya.MFnMatrixData( matrixObject )
    worldMatrix = worldMatrixData.matrix( )

    return worldMatrix


def decompMatrix(node,matrix):
    '''
    Decomposes a MMatrix in new api. Returns an list of translation,rotation,scale in world space.
    '''
    #Rotate order of object
    rotOrder = cmds.getAttr('%s.rotateOrder'%node)

    #Puts matrix into transformation matrix
    mTransformMtx = OpenMaya.MTransformationMatrix(matrix)

    #Translation Values
    trans = mTransformMtx.translation(OpenMaya.MSpace.kWorld)

    #Euler rotation value in radians
    eulerRot = mTransformMtx.rotation()
    
    eulerRot[0] = 0.0
    eulerRot[2] = 0.0
    print eulerRot, 'euler'
    #Reorder rotation order based on ctrl.
    eulerRot.reorderIt(rotOrder)

    #Find degrees
    angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]

    #Find world scale of our object.
    scale = mTransformMtx.scale(OpenMaya.MSpace.kWorld)

    #Return Values
    return [trans.x,trans.y,trans.z],angles,scale


def level():
    sel = cmds.ls(selection=True)
    
    if sel:
        for se in sel:
            _node = pm.PyNode(se)
            print _node
            do_level(se)


def do_flat(node):
    # store the world matrix
    
    #_world_matrix = node.getMatrix(worldSpace=True)
    _rot = pm.xform(query=True,worldSpace=True,rotation=True)
    print _rot
    # recall the worldSpace matrix
    pm.xform(worldSpace=True,rotation=_rot)
    # node.setMatrix(_world_matrix, worldSpace=True)
    node.rotateX.set(0.0)
    node.rotateZ.set(0.0)


def do_level(node):    
    _matrix = getMatrix(node)
    _original_matrix = OpenMaya.MTransformationMatrix(_matrix)
    # cache the rotate pivots

    _rp = pm.xform(node, query=True, rotatePivot=True)
    _lsp = pm.xform(node, query=True, scalePivot=True)
    
    scale = _original_matrix.scale(OpenMaya.MSpace.kWorld)

    print scale, 'scale'
    print _matrix
    rotOrder = cmds.getAttr('%s.rotateOrder'%node)
    _flat = [1.0, 0.0, 1.0]
    _up = dt.Vector([0,1,0])
    x_vector = dt.Vector([_matrix[0],_matrix[1],_matrix[2]])
    y_vector = dt.Vector([_matrix[4],_matrix[5],_matrix[6]])
    z_vector = dt.Vector([_matrix[8],_matrix[9],_matrix[10]])

    '''
    print dt.Vector.length(x_vector),'x vector mag'
    _flatX = multiply(x_vector,_flat)
    _flatZ = multiply(z_vector,_flat)
    
    _crossY = dt.Vector.cross_product(_flatZ,_flatX)
    _crossX = NT_Math.Vector.cross_product(_crossY,_flatZ)
    _crossZ = NT_Math.Vector.cross_product(_crossX,_crossY)
    
    _matrix = constructMatrix(_matrix,_crossX,_crossY,_crossZ)
    print _matrix ,'_matrix'
    mTransformMtx = OpenMaya.MTransformationMatrix(_matrix)
    print mTransformMtx.asMatrix(), 'mTransformMtx'
    eulerRot = mTransformMtx.rotation()
    eulerRot.reorderIt(rotOrder)
    angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
    print angles, '!!!!!'
    _node = pm.PyNode(node)
    _node.rotate.set(angles)
    '''
    '''
    _node.setMatrix(_matrix, worldSpace=True)
    pm.xform(node, rotatePivot=_rp)
    pm.xform(node, scalePivot=_lsp)
    pm.xform(node, scale=scale)
    '''
    #_node.rotate.set(angles)
    
    
def level_poop():
    sel = cmds.ls(selection=True)[0]
    _x = pm.PyNode('x')
    _y = pm.PyNode('y')
    _z = pm.PyNode('z')
    _x_flat = pm.PyNode('x_flat')
    _y_cross = pm.PyNode('y_cross')
    _x_cross = pm.PyNode('x_cross')
    _z_cross = pm.PyNode('z_cross')
    _z_flat = pm.PyNode('z_flat')
    _gizmo = pm.PyNode('gizmo')
    _matrix = getMatrix(sel)
    print _matrix

    _flat = [1.0, 0.0, 1.0]
    x_vector = [_matrix[0],_matrix[1],_matrix[2]]
    y_vector = [_matrix[4],_matrix[5],_matrix[6]]
    z_vector = [_matrix[8],_matrix[9],_matrix[10]]
    
    _flatX = multiply(x_vector,_flat)
    _flatZ = multiply(z_vector,_flat)
    
    _crossY = NT_Math.Vector.normalize(NT_Math.Vector.cross_product(_flatZ,_flatX))
    _crossX = NT_Math.Vector.normalize(NT_Math.Vector.cross_product(_crossY,_flatZ))
    _crossZ = NT_Math.Vector.normalize(NT_Math.Vector.cross_product(_crossX,_crossY))
    _x.attr('translateX').set(_matrix[0])
    _x.attr('translateY').set(_matrix[1])
    _x.attr('translateZ').set(_matrix[2])

    _y.attr('translateX').set(_matrix[4])
    _y.attr('translateY').set(_matrix[5])
    _y.attr('translateZ').set(_matrix[6])
    
    _z.attr('translateX').set(_matrix[8])
    _z.attr('translateY').set(_matrix[9])
    _z.attr('translateZ').set(_matrix[10]) 

    _x_flat.attr('translate').set(_flatX)
    _y_cross.attr('translate').set(_crossY)
    _z_flat.attr('translate').set(_flatZ)
    _x_cross.attr('translate').set(_crossX)
    _z_cross.attr('translate').set(_crossZ)
    
    _matrix = constructMatrix(_matrix,_crossX,_crossY,_crossZ)
    '''
    _matrix[0] = _crossX[0]
    _matrix[1] = _crossX[1]
    _matrix[2] = _crossX[2]
    _matrix[4] = _crossY[0]
    _matrix[5] = _crossY[1]
    _matrix[6] = _crossY[2]
    _matrix[8] = _crossZ[0]
    _matrix[9] = _crossZ[1]
    _matrix[10] = _crossZ[2]
    '''
    print _matrix
    _gizmo.setMatrix(_matrix, worldSpace=True)
    
def constructMatrix(_matrix, x_vector, y_vector, z_vector):
    _matrix[0] = x_vector[0]
    _matrix[1] = x_vector[1]
    _matrix[2] = x_vector[2]
    _matrix[4] = y_vector[0]
    _matrix[5] = y_vector[1]
    _matrix[6] = y_vector[2]
    _matrix[8] = z_vector[0]
    _matrix[9] = z_vector[1]
    _matrix[10] = z_vector[2]
    
    return _matrix

def multiply(input1, input2):
    input1 = NT_Math.Vector.normalize(input1)
    print 'input1, mag',NT_Math.Vector.magnitude(input1)
    input2 = NT_Math.Vector.normalize(input2)
    print 'input2, mag',NT_Math.Vector.magnitude(input2)
    _out = NT_Math.Vector.normalize([input1[0]*input2[0],input1[1]*input2[1],input1[2]*input2[2]])
    _mag = NT_Math.Vector.magnitude(_out)
    print 'vector ',_out,'\nmag',_mag
    return _out


def get_ma(data):
    return [ data[0],data[1],data[2]]

