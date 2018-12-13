import maya.cmds as cmds
import random
import math

def distance(point1, point2):
    return

# Centroidal Voronoi diagram
def cvd():
    print("hej")
    return

# Strain energy density
# Input = point on object
def sed(point):
    print("hej")
    return
    
# Distance weighted deformation energy
def dwde():
    print("hej")
    return


def cleanUpOld():
    cmds.select( all=True )
    cmds.delete()
  
def generateRandomPointWithinRadius(maxRadius, centerPoint):
    #Currently hardcoded for plane
    
    angle = random.random() * 2 * math.pi
    # Gaussian distribution: little chance of being outside 4 standard deviations
    # Choose radius which will most likely be within maxRadius
    radius = random.gauss(0, maxRadius * 0.25)
    x = centerPoint[0] + radius * math.cos(angle)
    y = centerPoint[1] + radius * math.sin(angle)
    return [x, y, centerPoint[2]]
    
def generateVoronoiPoints(fracturePosition): 
    maxRadius = 15
    centerPoints = []
    numPoints = 20
    
    for i in range(numPoints):
        centerPoints.append(generateRandomPointWithinRadius(maxRadius, fracturePosition))
    
    return centerPoints


    
def cutObject(object, voronoiPoints):
    # Cut according to Voronoi cells
    for from_point in voronoiPoints:
        #https://openmaya.quora.com/How-to-implement-Voronoi-with-Python-for-Maya
        print(from_point)
        working_geom = cmds.duplicate(object[0])
        for to_point in voronoiPoints:
            if from_point != to_point:
                locator = cmds.spaceLocator();
                cmds.move(from_point[0],from_point[1],from_point[2])
                cmds.parent(locator,working_geom)
                center_point = [(e1+e2)/2 for  (e1,e2) in zip(to_point,from_point)]
                n = [(e1-e2) for (e1,e2) in zip(from_point,to_point)]
                es = cmds.angleBetween( euler=True, v1=[0,0,1], v2=n )
                cmds.polyCut(working_geom, deleteFaces=True, cutPlaneCenter=center_point, cutPlaneRotate=es)
                cmds.polyCloseBorder(working_geom)
    cmds.delete(object)

cleanUpOld()

# Set up needed objects
myPlane = cmds.polyPlane( h=30, w=30, sx=5, sy=5, ax=(0, 0, 1), name='myPlane', cuv=2, ch=0 )

mySphere = cmds.polySphere( n='mySphere', sx=10, sy=10 )
cmds.setAttr('mySphere.translateZ', 10)

path = cmds.curve( d=1, p=[(0, 0, 20), (0, 0, -20)], k=[0, 1] )

cmds.pathAnimation( mySphere[0], stu=0, etu=60, c=path )

# Avoiding collision detection for now
sphereRaduis = cmds.polySphere( 'mySphere', q=True, sx=True )



''' Hard code test fracture '''
fracturePosition = cmds.objectCenter(myPlane, gl=True)
print("Fracture position is:")
print(fracturePosition)

centerPoints = generateVoronoiPoints(fracturePosition)
cutObject(myPlane, centerPoints)