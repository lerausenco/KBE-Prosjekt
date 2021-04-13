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

    def __init__(self, name, pipe_diam, lock_th):

        """
            Constructor. Initialises arguments and creates the part from cylinders and cones.
                args:
                    name [string] - name of part file
                    pipe_diam [float] - diameter of scaffolding pipes
                    lock_th [float] - thickness of "lock"
        """
        self.name = name
        self.pipe_diam = pipe_diam
        self.lock_th = lock_th
        self.session = NXOpen.Session.GetSession()
        self.workPart = self.session.Parts.Work
        self.jid = []

        self.make_new_file()

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
        print("JID LIST  ", self.jid)

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

        # make a list with the target body removed,
        # containing only the tool bodies
        self.tool_body_jid = self.jid[1:]

        bodies1 = [NXOpen.Body.Null] * len(self.tool_body_jid)

        for i in range(0,len(bodies1)):
            print("BODY ADDED: ", self.tool_body_jid[i])
            body = self.workPart.Bodies.FindObject(self.tool_body_jid[i])
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

    def make_new_file(self):
        displayPart = self.session.Parts.Display
        fileNew1 = self.session.Parts.FileNew()
           
        fileNew1.TemplateFileName = "model-plain-1-mm-template.prt"
        fileNew1.UseBlankTemplate = False
        fileNew1.ApplicationName = "ModelTemplate"
        fileNew1.Units = NXOpen.Part.Units.Millimeters
        fileNew1.RelationType = ""
        fileNew1.UsesMasterModel = "No"
        fileNew1.TemplateType = NXOpen.FileNewTemplateType.Item
        fileNew1.TemplatePresentationName = "Model"
        fileNew1.ItemType = ""
        fileNew1.Specialization = ""
        fileNew1.SetCanCreateAltrep(False)
        fileNew1.NewFileName = "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\temp_" + self.name + ".prt"
        fileNew1.MasterFileName = ""
        fileNew1.MakeDisplayedPart = True
        fileNew1.DisplayPartOption = NXOpen.DisplayPartOption.AllowAdditional
        nXObject1 = fileNew1.Commit()
        
        self.workPart = self.session.Parts.Work # model2
        fileNew1.Destroy()
    
    def save_part(self):
        displayPart = self.session.Parts.Display
        self.workPart.SaveAs("C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\" + self.name + ".prt")

        #alternative path
        #self.workPart.SaveAs("C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\" + self.name + ".prt")

    def make_fem_file(self):
        theSession  = NXOpen.Session.GetSession()
        workPart = theSession.Parts.Work
        displayPart = theSession.Parts.Display
        # ----------------------------------------------
        #   Menu: File->New...
        # ----------------------------------------------
        markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        fileNew1 = theSession.Parts.FileNew()
        
        theSession.SetUndoMarkName(markId1, "New Dialog")
        
        markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New")
        
        theSession.DeleteUndoMark(markId2, None)
        
        markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New")
        
        fileNew1.TemplateFileName = "FemNxNastranMetric.fem"
        
        fileNew1.UseBlankTemplate = False
        
        fileNew1.ApplicationName = "CaeFemTemplate"
        
        fileNew1.Units = NXOpen.Part.Units.Millimeters
        
        fileNew1.RelationType = ""
        
        fileNew1.UsesMasterModel = "No"
        
        fileNew1.TemplateType = NXOpen.FileNewTemplateType.Item
        
        fileNew1.TemplatePresentationName = "Simcenter Nastran"
        
        fileNew1.ItemType = ""
        
        fileNew1.Specialization = ""
        
        fileNew1.SetCanCreateAltrep(False)
        
        fileNew1.NewFileName = "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\fem_" + self.name + ".fem"
        
        fileNew1.MasterFileName = ""
        
        fileNew1.MakeDisplayedPart = True
        
        fileNew1.DisplayPartOption = NXOpen.DisplayPartOption.AllowAdditional
        
        baseTemplateManager1 = theSession.XYPlotManager.TemplateManager
        
        nXObject1 = fileNew1.Commit()
        
        workPart = NXOpen.Part.Null
        workFemPart = theSession.Parts.BaseWork
        displayPart = NXOpen.Part.Null
        displayFemPart = theSession.Parts.BaseDisplay
        theSession.DeleteUndoMark(markId3, None)
        
        fileNew1.Destroy()
        
        markId4 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        unit1 = workFemPart.UnitCollection.FindObject("MilliMeter")
        expression1 = workFemPart.Expressions.CreateSystemExpressionWithUnits("0.01", unit1)
        
        expression1.SetFormula("0.01")
        
        unit2 = workFemPart.UnitCollection.FindObject("Degrees")
        expression2 = workFemPart.Expressions.CreateSystemExpressionWithUnits("15", unit2)
        
        expression2.SetFormula("15")
        
        theSession.SetUndoMarkName(markId4, "New FEM Dialog")
        
        # ----------------------------------------------
        #   Dialog Begin New FEM
        # ----------------------------------------------
        markId5 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New FEM")
        
        theSession.DeleteUndoMark(markId5, None)
        
        markId6 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New FEM")
        
        femPart1 = workFemPart
        femPart1.PolygonGeometryMgr.SetPolygonBodyResolutionOnFemBodies(NXOpen.CAE.PolygonGeometryManager.PolygonBodyResolutionType.Standard)
        
        femPart2 = workFemPart
        femCreationOptions1 = femPart2.NewFemCreationOptions()
        
        femPart3 = workFemPart
        femSynchronizeOptions1 = femPart3.NewFemSynchronizeOptions()
        
        femSynchronizeOptions1.SynchronizePointsFlag = False
        
        femSynchronizeOptions1.SynchronizeCreateMeshPointsFlag = False
        
        femSynchronizeOptions1.SynchronizeCoordinateSystemFlag = False
        
        femSynchronizeOptions1.SynchronizeLinesFlag = False
        
        femSynchronizeOptions1.SynchronizeArcsFlag = False
        
        femSynchronizeOptions1.SynchronizeSplinesFlag = False
        
        femSynchronizeOptions1.SynchronizeConicsFlag = False
        
        femSynchronizeOptions1.SynchronizeSketchCurvesFlag = False
        
        femSynchronizeOptions1.SynchronizeDplaneFlag = False
        
        part1 = theSession.Parts.FindObject(self.name)
        femCreationOptions1.SetCadData(part1, "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\fem_"+self.name+"_i2.prt")
        
        bodies1 = [NXOpen.Body.Null] * 1 
        body1 = part1.Bodies.FindObject(self.jid[0])
        bodies1[0] = body1
        femCreationOptions1.SetGeometryOptions(NXOpen.CAE.FemCreationOptions.UseBodiesOption.VisibleBodies, bodies1, femSynchronizeOptions1)
        
        femCreationOptions1.SetSolverOptions("NX NASTRAN", "Structural", NXOpen.CAE.BaseFemPart.AxisymAbstractionType.NotSet)
        
        description1 = []
        femCreationOptions1.SetDescription(description1)
        
        femCreationOptions1.SetMorphingFlag(False)
        
        femCreationOptions1.SetCyclicSymmetryData(False, NXOpen.CoordinateSystem.Null)
        
        femPart4 = workFemPart
        femPart4.FinalizeCreation(femCreationOptions1)
        
        femSynchronizeOptions1.Dispose()
        femCreationOptions1.Dispose()
        theSession.DeleteUndoMark(markId6, None)
        
        theSession.ApplicationSwitchImmediate("UG_APP_SFEM")
        
        markId7 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Enter Pre/Post")
               
        
        markId8 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
        fEModel1 = workFemPart.FindObject("FEModel")
        meshManager1 = fEModel1.Find("MeshManager")
        mesh3dTetBuilder1 = meshManager1.CreateMesh3dTetBuilder(NXOpen.CAE.Mesh3d.Null)
        
        mesh3dTetBuilder1.ElementType.DestinationCollector.ElementContainer = NXOpen.CAE.MeshCollector.Null
        
        mesh3dTetBuilder1.ElementType.ElementTypeName = "CTETRA(10)"
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh overall edge size", "5", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("small feature value", "0.5", NXOpen.Unit.Null)
        
        theSession.SetUndoMarkName(markId8, "3D Tetrahedral Mesh Dialog")
        
        cAEBody1 = workFemPart.FindObject("CAE_Body(1)")
        added1 = mesh3dTetBuilder1.SelectionList.Add(cAEBody1)
        
        markId9 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "3D Tetrahedral Mesh")
        
        theSession.DeleteUndoMark(markId9, None)
        
        markId10 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "3D Tetrahedral Mesh")
        
        mesh3dTetBuilder1.AutoResetOption = False
        
        mesh3dTetBuilder1.ElementType.ElementDimension = NXOpen.CAE.ElementTypeBuilder.ElementType.FreeSolid
        
        mesh3dTetBuilder1.ElementType.ElementTypeName = "CTETRA(10)"
        
        destinationCollectorBuilder1 = mesh3dTetBuilder1.ElementType.DestinationCollector
        
        destinationCollectorBuilder1.ElementContainer = NXOpen.CAE.MeshCollector.Null
        
        destinationCollectorBuilder1.AutomaticMode = True
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh overall edge size", "5", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("mapped mesh option bool", True)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("multiblock cylinder option bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("fillet num elements", 3)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("num elements on cylinder circumference", 6)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("element size on cylinder height", "1", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("create pyramids bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("midnodes", 0)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("geometry tolerance option bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("geometry tolerance", "0", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("max jacobian", "10", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("surface mesh size variation", "50", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("volume mesh size variation", "50", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("internal mesh gradation", "1.05", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("internal max edge option bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("internal max edge length value", "0", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("two elements through thickness bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("mesh transition bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("remesh on bad quality bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("maximum edge length bool", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("maximum edge length", "1", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("small feature tolerance", "10", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("small feature value", "0.5", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("boundary layer element type", 3)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("insert blend elements", True)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("blending angle", "90", unit2)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("sweep angle", "45", unit2)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("control aspect ratio", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("maximum exposed aspect ratio", "1000", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("control slender", False)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("minimum aspect ratio", "0.01", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("maximum imprint dihedral angle", "150", unit2)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("gradation rate", "10", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("smoothing distance factor", "3", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("all-tet boundary layer", False)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("dont format mesh to solver", 0)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh edge match tolerance", "0.02", NXOpen.Unit.Null)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh smoothness tolerance", "0.01", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("min face angle", "20", unit2)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("mesh time stamp", 0)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh node coincidence tolerance", "0.0001", unit1)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("mesh edit allowed", 0)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("edge angle", "15", unit2)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("merge edge toggle", 0)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("auto constraining", 1)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("curvature scaling", 1)
        
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("target angle", "45", unit2)
        
        mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("edge shape", 2)
        
        id1 = theSession.NewestVisibleUndoMark
        
        nErrs1 = theSession.UpdateManager.DoUpdate(id1)
        
        meshes1 = mesh3dTetBuilder1.CommitMesh()
        
        theSession.DeleteUndoMark(markId10, None)
        
        theSession.SetUndoMarkName(id1, "3D Tetrahedral Mesh")
        
        mesh3dTetBuilder1.Destroy()


        
name = "partfemmesh6"
myduralok = Duralok(name, pipe_diam, lock_th)
myduralok.save_part()
myduralok.make_fem_file()



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