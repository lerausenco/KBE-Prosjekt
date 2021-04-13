from shapes.Block import Block
from shapes.Cylinder import Cylinder
from shapes.Cone import Cone
from utils.Analyzer import Analyzer
from datetime import datetime
import math
from math import sin, cos, radians
import time
import random

import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities

import math
import NXOpen
import NXOpen.Assemblies
import NXOpen.CAE
import NXOpen.Fields
import NXOpen.MenuBar
import NXOpen.PhysMat

parts_list = []

pipe_diam = 40
lock_th = pipe_diam/10

class Duralok:

    def __init__(self, pipe_diam, lock_th):

        """
            Constructor. Initialises arguments and creates the part from cylinders and cones.
                args:
                    pipe_diam [float] - diameter of scaffolding pipes
                    lock_th [float] - thickness of "lock"
        """

        self.pipe_diam = pipe_diam
        self.lock_th = lock_th
        self.session = NXOpen.Session.GetSession()
        self.workPart = self.session.Parts.Work
        self.jid = []


        #make shapes needed to create model
        #TOP CONE
        top_cone = Cone(
            x=0,y=0,z=self.pipe_diam/2+self.lock_th, 
            baseDiameter=self.lock_th*6+self.pipe_diam,
            topDiameter=self.pipe_diam+2*self.lock_th,
            height=self.pipe_diam/2,
            direction= [0,0,1],
            color="BLUE",
            material="Steel") 

        parts_list.append(top_cone)

        hollow_top_cone = Cylinder(
            x=top_cone.x,y=top_cone.y,z=top_cone.z,
            diameter=self.pipe_diam,
            height=top_cone.height*2,
            direction=[0,0,1],
            color="GRAY",
            material="STEEL"
        )
        parts_list.append(hollow_top_cone)


        #TOP CYL
        top_cyl = Cylinder(
            x=0,y=0,z=top_cone.z+top_cone.height,
            diameter=top_cone.topDiameter,
            height=self.pipe_diam/5,
            direction=[0,0,1],
            color="BLUE",
            material="Steel"
        )

        parts_list.append(top_cyl)

        hollow_top_cyl = Cylinder(
            x=top_cyl.x,y=top_cyl.y,z=top_cyl.z,
            diameter=self.pipe_diam,
            height=top_cyl.height,
            direction=[0,0,1],
            color="GRAY",
            material="STEEL"
        )
        parts_list.append(hollow_top_cyl)


        side_stiff_width = (top_cone.baseDiameter - top_cone.topDiameter)/2
        w = side_stiff_width

        for i in range(6):
            y = cos(radians(i*60))*(top_cone.baseDiameter-w)/2 
            x = sin(radians(i*60))*(top_cone.baseDiameter-w)/2

            side_cyl = Cylinder(
                x=x, y=y, z=top_cone.z,
                diameter=w,
                height=top_cone.height,
                color="BLUE",
                material="Steel",
                direction=[0,0,1]
            )
            parts_list.append(side_cyl)


        #bottom cone 1
        bottom_cone1 = Cone(
            x=0,y=0,z=-top_cone.z,
            baseDiameter=top_cone.baseDiameter,
            topDiameter=top_cone.baseDiameter*0.85,
            height=8,
            direction=[0,0,-1],
            color="BLUE",
            material="STEEL",
        )

        parts_list.append(bottom_cone1)

        hollow_bottom_cone1 = Cylinder(
            x=0,y=0,z=bottom_cone1.z,
            diameter=self.pipe_diam,
            height=bottom_cone1.height,
            direction=bottom_cone1.direction,
            color="GREY",
            material="STEEL"
        )
        parts_list.append(hollow_bottom_cone1)

        #bottom cone 2

        bottom_cone2 = Cone(
            x=0,y=0,z=-top_cone.z-bottom_cone1.height,
            baseDiameter=bottom_cone1.topDiameter,
            topDiameter=self.pipe_diam+2*self.lock_th,
            height=15,
            direction=[0,0,-1],
            color="BLUE",
            material="STEEL"
        )

        parts_list.append(bottom_cone2)

        hollow_bottom_cone2 = Cylinder(
            x=0,y=0,z=bottom_cone2.z,
            diameter=self.pipe_diam,
            height=bottom_cone2.height,
            direction=bottom_cone2.direction,
            color="GREY",
            material="STEEL"
        )
        parts_list.append(hollow_bottom_cone2)


        space_between_cones = top_cone.z - bottom_cone1.z

        #hollow through other crossing cyl
        hollow_cross_2 = Cylinder(
            x = top_cone.x, y=top_cone.y, z=top_cone.z,
            diameter=self.pipe_diam,
            height=space_between_cones,
            direction=[0,0,-1],
            color="GREY",
            material="STEEL"
        )

        parts_list.append(hollow_cross_2)


        #outer cylinder part of the construction
        middle_cyl = Cylinder(
            x=0,y=0,z=bottom_cone1.z,
            diameter=bottom_cone1.baseDiameter,
            height=space_between_cones,
            direction=[0,0,1],
            color="YELLOW",
            material="STEEL"
        )
        parts_list.append(middle_cyl)

        #hollow through middle cylinder
        hollow_middle_cyl = Cylinder(
            x=0,y=0,z=middle_cyl.z,
            diameter=self.pipe_diam,
            height=middle_cyl.height,
            direction=middle_cyl.direction,
            color="GRAY",
            material="STEEL"
        )
        parts_list.append(hollow_middle_cyl)

        side_opening_1 = Cylinder(
            x=-top_cone.baseDiameter/2, y=0, z = 0,
            diameter=self.pipe_diam+2*self.lock_th,
            height=top_cone.baseDiameter,
            direction=[1,0,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_opening_1)

        #hollow through crossing tubes
        hollow_cross_1 = Cylinder(
            x = top_cone.x, y=top_cone.y, z=top_cone.z,
            diameter=self.pipe_diam,
            height=space_between_cones,
            direction=[0,0,-1],
            color="GREY",
            material="STEEL"
        )

        parts_list.append(hollow_cross_1)


        #FOR SUBTRACTION
        side_pipe_1 = Cylinder(
            x=-top_cone.baseDiameter/2-self.lock_th, y=0, z = 0,
            diameter=self.pipe_diam,
            height=top_cone.baseDiameter+2*self.lock_th,
            direction=[1,0,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_pipe_1)


        # more copies to perform subtraction
        side_pipe_1_1 = Cylinder(
            x=-top_cone.baseDiameter/2, y=0, z = 0,
            diameter=self.pipe_diam,
            height=top_cone.baseDiameter,
            direction=[1,0,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_pipe_1_1)


        side_pipe_1_2 = Cylinder(
            x=-top_cone.baseDiameter/2, y=0, z = 0,
            diameter=self.pipe_diam,
            height=top_cone.baseDiameter,
            direction=[1,0,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_pipe_1_2)


        side_opening_2 = Cylinder(
            x=0, y=-top_cone.baseDiameter/2, z = 0,
            diameter=self.pipe_diam+2*self.lock_th,
            height=top_cone.baseDiameter,
            direction=[0,1,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_opening_2)


        #for subtraction
        side_pipe_2 = Cylinder(
            x=0, y=-top_cone.baseDiameter/2, z = 0,
            diameter=self.pipe_diam,
            height=top_cone.baseDiameter,
            direction=[0,1,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_pipe_2)

        #need more copies to perform subtraction
        side_pipe_2_1 = Cylinder(
            x=0, y=-top_cone.baseDiameter/2, z = 0,
            diameter=self.pipe_diam,
            height=top_cone.baseDiameter,
            direction=[0,1,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_pipe_2_1)

        side_pipe_2_2 = Cylinder(
            x=0, y=-top_cone.baseDiameter/2, z = 0,
            diameter=self.pipe_diam,
            height=top_cone.baseDiameter,
            direction=[0,1,0],
            color="YELLOW",
            material="STEEL"
        )

        parts_list.append(side_pipe_2_2)

        #initialise all features in the list
        for part in parts_list:
            body = part.initForNX()

        #subtractions
        hollow_top_cone.subtractFrom(top_cone)
        hollow_top_cyl.subtractFrom(top_cyl) 

        hollow_bottom_cone1.subtractFrom(bottom_cone1)
        hollow_bottom_cone2.subtractFrom(bottom_cone2)

        hollow_middle_cyl.subtractFrom(middle_cyl)

        side_pipe_2_1.subtractFrom(side_opening_1)
        side_pipe_1_2.subtractFrom(side_opening_1)

        side_pipe_2_2.subtractFrom(side_opening_2)
        side_pipe_1_1.subtractFrom(side_opening_2)

        side_pipe_1.subtractFrom(middle_cyl)
        side_pipe_2.subtractFrom(middle_cyl)

        hollow_cross_1.subtractFrom(side_opening_1)
        hollow_cross_2.subtractFrom(side_opening_2)

        self.get_objects_to_unite()
        self.unite_all()
        
    def get_objects_to_unite(self):
        
        objects = self.workPart.Layers.GetAllObjectsOnLayer(1)

        for object in objects:
            try:			
                if object.IsSolidBody:
                    self.jid.append(str(object.JournalIdentifier))
            except Exception as e:
                    pass
        #remove all objects containing string "ENTITY" as they are not used in
        # unite operation        
        self.jid = [x for x in self.jid if not "ENTITY" in x]

    def unite_all(self):
        booleanBuilder1 = self.workPart.Features.CreateBooleanBuilderUsingCollector(NXOpen.Features.BooleanFeature.Null)
        scCollector1 = booleanBuilder1.ToolBodyCollector
        booleanRegionSelect1 = booleanBuilder1.BooleanRegionSelect
        booleanBuilder1.Tolerance = 0.01
        booleanBuilder1.Operation = NXOpen.Features.Feature.BooleanType.Unite

        #assign the first body in the list as the target body
        body1 = self.workPart.Bodies.FindObject(self.jid[0])
        added1 = booleanBuilder1.Targets.Add(body1)
        targets1 = [NXOpen.TaggedObject.Null] * 1 
        targets1[0] = body1
        booleanRegionSelect1.AssignTargets(targets1)

        #collect the rest of the bodies to unite them
        scCollector2 = self.workPart.ScCollectors.CreateCollector()
        bodies1 = [NXOpen.Body.Null] * (len(self.jid) - 1)

        for i in range(0,len(bodies1)):
            body = self.workPart.Bodies.FindObject(self.jid[i])
            bodies1[i] = body

        #complete the unite operation
        bodyDumbRule1 = self.workPart.ScRuleFactory.CreateRuleBodyDumb(bodies1, True)
        rules1 = [None] * 1 
        rules1[0] = bodyDumbRule1
        scCollector2.ReplaceRules(rules1, False)

        booleanBuilder1.ToolBodyCollector = scCollector2
        targets2 = [NXOpen.TaggedObject.Null] * 1 
        targets2[0] = body1
        booleanRegionSelect1.AssignTargets(targets2)

        nXObject1 = booleanBuilder1.Commit()
        booleanBuilder1.Destroy()
    
    def save_part(self, name):
        displayPart = self.session.Parts.Display
        self.workPart.SaveAs("C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\" + name + ".prt")

        #alternative path
        #self.workPart.SaveAs("C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\" + name + ".prt")


myduralok = Duralok(pipe_diam, lock_th)
myduralok.save_part("mynamedduralok2")

"""
def getFaces(self):
    theSession  = NXOpen.Session.GetSession()
    #workPart = theSession.Parts.Work
    
    for partObject in theSession.Parts:
        self.processPart(partObject)
    
def processPart(self, partObject):
    for bodyObject in partObject.Bodies:
        self.processBodyFaces(bodyObject)
        #processBodyEdges(bodyObject)
        
def processBodyFaces(self, bodyObject):
    for faceObject in bodyObject.GetFaces():
        self.processFace(faceObject)
        
def processFace(self, faceObject):
    print("Face found.")
    for edgeObject in faceObject.GetEdges():
        self.processEdge(edgeObject)
    
def processEdge(self, edgeObject):
    #Printing vertices
    v1 = edgeObject.GetVertices()[0]
    v2 = edgeObject.GetVertices()[1] 
    print("Vertex 1:", v1)
    print("Vertex 2:", v2)
"""