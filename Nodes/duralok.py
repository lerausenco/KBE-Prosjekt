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

    def make_fem_model(self):
        self.session  = NXOpen.Session.GetSession()
        self.workPart = self.session.Parts.Work
        displayPart = self.session.Parts.Display
             
        
        fileNew1 = self.session.Parts.FileNew()
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
        baseTemplateManager1 = self.session.XYPlotManager.TemplateManager
        nXObject1 = fileNew1.Commit()
        
        self.workPart = NXOpen.Part.Null
        workFemPart = self.session.Parts.BaseWork
        displayPart = NXOpen.Part.Null
        displayFemPart = self.session.Parts.BaseDisplay
        
        fileNew1.Destroy()
        
        unit1 = workFemPart.UnitCollection.FindObject("MilliMeter")
        expression1 = workFemPart.Expressions.CreateSystemExpressionWithUnits("0.01", unit1)
        expression1.SetFormula("0.01")
        unit2 = workFemPart.UnitCollection.FindObject("Degrees")
        expression2 = workFemPart.Expressions.CreateSystemExpressionWithUnits("15", unit2)
        expression2.SetFormula("15")
        
    
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
        
        part1 = self.session.Parts.FindObject(self.name)
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
        
        self.session.ApplicationSwitchImmediate("UG_APP_SFEM")
        
        #mesh the part
        fEModel1 = workFemPart.FindObject("FEModel")
        meshManager1 = fEModel1.Find("MeshManager")
        mesh3dTetBuilder1 = meshManager1.CreateMesh3dTetBuilder(NXOpen.CAE.Mesh3d.Null)
        mesh3dTetBuilder1.ElementType.DestinationCollector.ElementContainer = NXOpen.CAE.MeshCollector.Null
        mesh3dTetBuilder1.ElementType.ElementTypeName = "CTETRA(10)"
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh overall edge size", "5", unit1)
        mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("small feature value", "0.5", NXOpen.Unit.Null)
        
      
        cAEBody1 = workFemPart.FindObject("CAE_Body(1)")
        added1 = mesh3dTetBuilder1.SelectionList.Add(cAEBody1)
        
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
        meshes1 = mesh3dTetBuilder1.CommitMesh()
        mesh3dTetBuilder1.Destroy()

    def do_sim(self):
        theSession  = NXOpen.Session.GetSession()
        workFemPart = theSession.Parts.BaseWork
        displayFemPart = theSession.Parts.BaseDisplay
        # ----------------------------------------------
        #   Menu: Application->Simulation->Design Simulation
        # ----------------------------------------------
        markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Enter Design Simulation")
        
        theSession.ApplicationSwitchImmediate("UG_APP_DESFEM")
        
        markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Enter Design Simulation")
        
        # ----------------------------------------------
        #   Menu: Tools->Materials->Assign Materials...
        # ----------------------------------------------
        markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        physicalMaterialListBuilder1 = workFemPart.MaterialManager.PhysicalMaterials.CreateListBlockBuilder()
        
        physicalMaterialAssignBuilder1 = workFemPart.MaterialManager.PhysicalMaterials.CreateMaterialAssignBuilder()
        
        theSession.SetUndoMarkName(markId3, "Assign Material Dialog")
        
        id1 = theSession.GetNewestUndoMark(NXOpen.Session.MarkVisibility.AnyVisibility)
        
        markId4 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Assign Material")
        
        theSession.DeleteUndoMark(markId4, None)
        
        markId5 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Assign Material")
        
        physicalMaterial1 = workFemPart.MaterialManager.PhysicalMaterials.LoadFromNxmatmllibrary("AISI_Steel_4340")
        
        objects1 = [NXOpen.NXObject.Null] * 1 
        cAEBody1 = workFemPart.FindObject("CAE_Body(1)")
        objects1[0] = cAEBody1
        physicalMaterial1.AssignObjects(objects1)
        
        theSession.DeleteUndoMark(markId5, None)
        
        theSession.SetUndoMarkName(id1, "Assign Material")
        
        physicalMaterialAssignBuilder1.Destroy()
        
        physicalMaterialListBuilder1.Destroy()
        
        # ----------------------------------------------
        #   Menu: File->New...
        # ----------------------------------------------
        markId6 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        fileNew1 = theSession.Parts.FileNew()
        
        theSession.SetUndoMarkName(markId6, "New Dialog")
        
        markId7 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New")
        
        theSession.DeleteUndoMark(markId7, None)
        
        markId8 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New")
        
        fileNew1.TemplateFileName = "SimNxNastranMetric.sim"
        
        fileNew1.UseBlankTemplate = False
        
        fileNew1.ApplicationName = "CaeSimTemplate"
        
        fileNew1.Units = NXOpen.Part.Units.Millimeters
        
        fileNew1.RelationType = ""
        
        fileNew1.UsesMasterModel = "No"
        
        fileNew1.TemplateType = NXOpen.FileNewTemplateType.Item
        
        fileNew1.TemplatePresentationName = "Simcenter Nastran"
        
        fileNew1.ItemType = ""
        
        fileNew1.Specialization = ""
        
        fileNew1.SetCanCreateAltrep(False)
        
        fileNew1.NewFileName = "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\sim1.sim"
        
        fileNew1.MasterFileName = ""
        
        fileNew1.MakeDisplayedPart = True
        
        fileNew1.DisplayPartOption = NXOpen.DisplayPartOption.AllowAdditional
        
        baseTemplateManager1 = theSession.XYPlotManager.TemplateManager
        
        nXObject1 = fileNew1.Commit()
        
        workSimPart = theSession.Parts.BaseWork
        displaySimPart = theSession.Parts.BaseDisplay
        theSession.DeleteUndoMark(markId8, None)
        
        fileNew1.Destroy()
        
        markId9 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        theSession.SetUndoMarkName(markId9, "New Simulation Dialog")
        
        # ----------------------------------------------
        #   Dialog Begin New Simulation
        # ----------------------------------------------
        markId10 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New Simulation")
        
        theSession.DeleteUndoMark(markId10, None)
        
        markId11 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "New Simulation")
        
        simPart1 = workSimPart
        femPart1 = theSession.Parts.FindObject("fem_"+self.name)
        description1 = []
        simPart1.FinalizeCreation(femPart1, 0, description1)
        
        theSession.DeleteUndoMark(markId11, None)
        
        markId12 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        simPart2 = workSimPart
        simSimulation1 = simPart2.Simulation
        
        simSolution1 = simSimulation1.CreateSolution("NX NASTRAN DESIGN", "Structural", "Linear Statics - Single Constraint", "Solution 1", NXOpen.CAE.SimSimulation.AxisymAbstractionType.NotSet)
        
        propertyTable1 = simSolution1.PropertyTable
        
        theSession.SetUndoMarkName(markId12, "Solution Dialog")
        
        # ----------------------------------------------
        #   Dialog Begin Solution
        # ----------------------------------------------
        markId13 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Solution")
        
        theSession.DeleteUndoMark(markId13, None)
        
        markId14 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Solution")
        
        markId15 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, None)
        
        simSolution1.Rename("Solution 1", False)
        
        propertyTable2 = simSolution1.PropertyTable
        
        id2 = theSession.NewestVisibleUndoMark
        
        nErrs1 = theSession.UpdateManager.DoUpdate(id2)
        
        simSolutionStep1 = simSolution1.CreateStep(0, True, "Subcase - Static Loads 1")
        
        nErrs2 = theSession.UpdateManager.DoUpdate(markId15)
        
        theSession.DeleteUndoMark(markId15, None)
        
        theSession.DeleteUndoMark(markId14, None)
        
        theSession.SetUndoMarkName(id2, "Solution")
        
        markId16 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        simPart3 = workSimPart
        simSimulation2 = simPart3.Simulation
        
        simBCBuilder1 = simSimulation2.CreateBcBuilderForConstraintDescriptor("fixedConstraint", "Fixed(1)", 1)
        
        propertyTable3 = simBCBuilder1.PropertyTable
        
        setManager1 = simBCBuilder1.TargetSetManager
        
        fieldExpression1 = propertyTable3.GetScalarFieldPropertyValue("DOF1")
        
        fieldExpression2 = propertyTable3.GetScalarFieldPropertyValue("DOF2")
        
        fieldExpression3 = propertyTable3.GetScalarFieldPropertyValue("DOF3")
        
        fieldExpression4 = propertyTable3.GetScalarFieldPropertyValue("DOF4")
        
        fieldExpression5 = propertyTable3.GetScalarFieldPropertyValue("DOF5")
        
        fieldExpression6 = propertyTable3.GetScalarFieldPropertyValue("DOF6")
        
        theSession.SetUndoMarkName(markId16, "Fixed Constraint Dialog")
        
        # ----------------------------------------------
        #   Dialog Begin Fixed Constraint
        # ----------------------------------------------
        rotMatrix1 = NXOpen.Matrix3x3()
        
        rotMatrix1.Xx = 0.4832982108266079
        rotMatrix1.Xy = 0.87536555473942901
        rotMatrix1.Xz = -0.012569207911850575
        rotMatrix1.Yx = 0.60732132160288466
        rotMatrix1.Yy = -0.32489835974270148
        rotMatrix1.Yz = 0.72498404683346596
        rotMatrix1.Zx = 0.63054234729978731
        rotMatrix1.Zy = -0.35801704067297407
        rotMatrix1.Zz = -0.6886509615541393
        translation1 = NXOpen.Point3d(0.031423019779619289, -1.8124601170836623, 1.7216274038853521)
        workSimPart.ModelingViews.WorkView.SetRotationTranslationScale(rotMatrix1, translation1, 1.6323272283886301)
        
        markId17 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Fixed Constraint")
        
        theSession.DeleteUndoMark(markId17, None)
        
        markId18 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Fixed Constraint")
        
        objects2 = [None] * 1 
        objects2[0] = NXOpen.CAE.SetObject()
        component1 = workSimPart.ComponentAssembly.RootComponent.FindObject("COMPONENT fem_"+self.name+" 1")
        cAEFace1 = component1.FindObject("PROTO#CAE_Body(1)|CAE_Face(17)")
        objects2[0].Obj = cAEFace1
        objects2[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
        objects2[0].SubId = 0
        setManager1.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects2)
        
        unit1 = workSimPart.UnitCollection.FindObject("MilliMeter")
        indepVarArray1 = []
        fieldExpression1.EditFieldExpression("0", unit1, indepVarArray1, False)
        
        propertyTable3.SetScalarFieldPropertyValue("DOF1", fieldExpression1)
        
        indepVarArray2 = []
        fieldExpression2.EditFieldExpression("0", unit1, indepVarArray2, False)
        
        propertyTable3.SetScalarFieldPropertyValue("DOF2", fieldExpression2)
        
        indepVarArray3 = []
        fieldExpression3.EditFieldExpression("0", unit1, indepVarArray3, False)
        
        propertyTable3.SetScalarFieldPropertyValue("DOF3", fieldExpression3)
        
        unit2 = workSimPart.UnitCollection.FindObject("Degrees")
        indepVarArray4 = []
        fieldExpression4.EditFieldExpression("0", unit2, indepVarArray4, False)
        
        propertyTable3.SetScalarFieldPropertyValue("DOF4", fieldExpression4)
        
        indepVarArray5 = []
        fieldExpression5.EditFieldExpression("0", unit2, indepVarArray5, False)
        
        propertyTable3.SetScalarFieldPropertyValue("DOF5", fieldExpression5)
        
        indepVarArray6 = []
        fieldExpression6.EditFieldExpression("0", unit2, indepVarArray6, False)
        
        propertyTable3.SetScalarFieldPropertyValue("DOF6", fieldExpression6)
        
        propertyValue1 = []
        propertyTable3.SetTextPropertyValue("description", propertyValue1)
        
        simBCBuilder1.DestinationFolder = NXOpen.CAE.SimLbcFolder.Null
        
        simBC1 = simBCBuilder1.CommitAddBc()
        
        simBCBuilder1.Destroy()
        
        theSession.DeleteUndoMark(markId18, None)
        
        theSession.SetUndoMarkName(markId16, "Fixed Constraint")
        
        rotMatrix2 = NXOpen.Matrix3x3()
        
        rotMatrix2.Xx = 0.51915138999780475
        rotMatrix2.Xy = 0.8541163572302759
        rotMatrix2.Xz = 0.031097951299576466
        rotMatrix2.Yx = -0.66471866167906724
        rotMatrix2.Yy = 0.38062480292733686
        rotMatrix2.Yz = 0.64286379600356769
        rotMatrix2.Zx = 0.53724383205294901
        rotMatrix2.Zy = -0.35441502184333279
        rotMatrix2.Zz = 0.7653489774036768
        translation2 = NXOpen.Point3d(-0.044610279273653464, -1.6694722584174295, -0.81007866948087792)
        workSimPart.ModelingViews.WorkView.SetRotationTranslationScale(rotMatrix2, translation2, 1.6323272283886301)
        
        markId19 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        simPart4 = workSimPart
        simSimulation3 = simPart4.Simulation
        
        simBCBuilder2 = simSimulation3.CreateBcBuilderForLoadDescriptor("magnitudeDirectionForce", "Force(1)", 1)
        
        propertyTable4 = simBCBuilder2.PropertyTable
        
        setManager2 = simBCBuilder2.TargetSetManager
        
        theSession.SetUndoMarkName(markId19, "Force Dialog")
        
        # ----------------------------------------------
        #   Dialog Begin Force
        # ----------------------------------------------
        expression1 = workSimPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
        
        origin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
        vector1 = NXOpen.Vector3d(-0.0, -0.0, -1.0)
        direction1 = workSimPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.AfterModeling)
        
        markId20 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Force")
        
        theSession.DeleteUndoMark(markId20, None)
        
        markId21 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Force")
        
        objects3 = [None] * 1 
        objects3[0] = NXOpen.CAE.SetObject()
        cAEFace2 = component1.FindObject("PROTO#CAE_Body(1)|CAE_Face(30)")
        objects3[0].Obj = cAEFace2
        objects3[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
        objects3[0].SubId = 0
        setManager2.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects3)
        
        unit3 = workSimPart.UnitCollection.FindObject("Newton")
        expression2 = workSimPart.Expressions.CreateSystemExpressionWithUnits("1000", unit3)
        
        fieldManager1 = workSimPart.FindObject("FieldManager")
        scalarFieldWrapper1 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression2)
        
        scalarFieldWrapper2 = propertyTable4.GetScalarFieldWrapperPropertyValue("TotalForce")
        
        expression3 = workSimPart.Expressions.CreateSystemExpressionWithUnits("1000", unit3)
        
        scalarFieldWrapper3 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression3)
        
        propertyTable4.SetScalarFieldWrapperPropertyValue("TotalForce", scalarFieldWrapper3)
        
        field1 = scalarFieldWrapper3.GetField()
        
        propertyTable4.SetVectorPropertyValue("Local Axis", direction1)
        
        propertyValue2 = []
        propertyTable4.SetTextPropertyValue("description", propertyValue2)
        
        simBCBuilder2.DestinationFolder = NXOpen.CAE.SimLbcFolder.Null
        
        simBC2 = simBCBuilder2.CommitAddBc()
        
        simBCBuilder2.Destroy()
        
        theSession.DeleteUndoMark(markId21, None)
        
        theSession.SetUndoMarkName(markId19, "Force")
        
        workSimPart.Expressions.Delete(expression1)
        
        markId22 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        simPart5 = workSimPart
        simSimulation4 = simPart5.Simulation
        
        simBCBuilder3 = simSimulation4.CreateBcBuilderForLoadDescriptor("magnitudeDirectionForce", "Force(2)", 2)
        
        propertyTable5 = simBCBuilder3.PropertyTable
        
        setManager3 = simBCBuilder3.TargetSetManager
        
        theSession.SetUndoMarkName(markId22, "Force Dialog")
        
        # ----------------------------------------------
        #   Dialog Begin Force
        # ----------------------------------------------
        expression4 = workSimPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
        
        origin2 = NXOpen.Point3d(0.0, 0.0, 0.0)
        vector2 = NXOpen.Vector3d(1.0, 0.0, 0.0)
        direction2 = workSimPart.Directions.CreateDirection(origin2, vector2, NXOpen.SmartObject.UpdateOption.AfterModeling)
        
        markId23 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Force")
        
        theSession.DeleteUndoMark(markId23, None)
        
        markId24 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Force")
        
        objects4 = [None] * 1 
        objects4[0] = NXOpen.CAE.SetObject()
        cAEFace3 = component1.FindObject("PROTO#CAE_Body(1)|CAE_Face(43)")
        objects4[0].Obj = cAEFace3
        objects4[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
        objects4[0].SubId = 0
        setManager3.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects4)
        
        expression5 = workSimPart.Expressions.CreateSystemExpressionWithUnits("900", unit3)
        
        scalarFieldWrapper4 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression5)
        
        scalarFieldWrapper5 = propertyTable5.GetScalarFieldWrapperPropertyValue("TotalForce")
        
        expression6 = workSimPart.Expressions.CreateSystemExpressionWithUnits("900", unit3)
        
        scalarFieldWrapper6 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression6)
        
        propertyTable5.SetScalarFieldWrapperPropertyValue("TotalForce", scalarFieldWrapper6)
        
        field2 = scalarFieldWrapper6.GetField()
        
        propertyTable5.SetVectorPropertyValue("Local Axis", direction2)
        
        propertyValue3 = []
        propertyTable5.SetTextPropertyValue("description", propertyValue3)
        
        simBCBuilder3.DestinationFolder = NXOpen.CAE.SimLbcFolder.Null
        
        simBC3 = simBCBuilder3.CommitAddBc()
        
        simBCBuilder3.Destroy()
        
        theSession.DeleteUndoMark(markId24, None)
        
        theSession.SetUndoMarkName(markId22, "Force")
        
        workSimPart.Expressions.Delete(expression4)
        
        markId25 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        simPart6 = workSimPart
        simSimulation5 = simPart6.Simulation
        
        simBCBuilder4 = simSimulation5.CreateBcBuilderForLoadDescriptor("torqueForce", "Torque(1)", 1)
        
        propertyTable6 = simBCBuilder4.PropertyTable
        
        setManager4 = simBCBuilder4.TargetSetManager
        
        theSession.SetUndoMarkName(markId25, "Torque Dialog")
        
        # ----------------------------------------------
        #   Dialog Begin Torque
        # ----------------------------------------------
        markId26 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Torque")
        
        theSession.DeleteUndoMark(markId26, None)
        
        markId27 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Torque")
        
        objects5 = [None] * 1 
        objects5[0] = NXOpen.CAE.SetObject()
        objects5[0].Obj = cAEFace3
        objects5[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
        objects5[0].SubId = 0
        setManager4.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomCylFace, objects5)
        
        unit4 = workSimPart.UnitCollection.FindObject("NewtonMeter")
        expression7 = workSimPart.Expressions.CreateSystemExpressionWithUnits("500", unit4)
        
        scalarFieldWrapper7 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression7)
        
        scalarFieldWrapper8 = propertyTable6.GetScalarFieldWrapperPropertyValue("TotalForce")
        
        expression8 = workSimPart.Expressions.CreateSystemExpressionWithUnits("500", unit4)
        
        scalarFieldWrapper9 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression8)
        
        propertyTable6.SetScalarFieldWrapperPropertyValue("TotalForce", scalarFieldWrapper9)
        
        field3 = scalarFieldWrapper9.GetField()
        
        propertyValue4 = []
        propertyTable6.SetTextPropertyValue("description", propertyValue4)
        
        simBCBuilder4.DestinationFolder = NXOpen.CAE.SimLbcFolder.Null
        
        simBC4 = simBCBuilder4.CommitAddBc()
        
        simBCBuilder4.Destroy()
        
        theSession.DeleteUndoMark(markId27, None)
        
        theSession.SetUndoMarkName(markId25, "Torque")
        
        # ----------------------------------------------
        #   Menu: Analysis->Solve...
        # ----------------------------------------------
        markId28 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
        
        theSession.SetUndoMarkName(markId28, "Solve Dialog")
        
        markId29 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Solve")
        
        theSession.DeleteUndoMark(markId29, None)
        
        markId30 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Solve")
        
        theCAESimSolveManager = NXOpen.CAE.SimSolveManager.GetSimSolveManager(theSession)
        
        psolutions1 = [NXOpen.CAE.SimSolution.Null] * 1 
        psolutions1[0] = simSolution1
        numsolutionssolved1, numsolutionsfailed1, numsolutionsskipped1 = theCAESimSolveManager.SolveChainOfSolutions(psolutions1, NXOpen.CAE.SimSolution.SolveOption.Solve, NXOpen.CAE.SimSolution.SetupCheckOption.CompleteCheckAndOutputErrors, NXOpen.CAE.SimSolution.SolveMode.Background)
        
        theSession.DeleteUndoMark(markId30, None)
        
        theSession.SetUndoMarkName(markId28, "Solve")

        time.sleep(30)
        
        simResultReference1 = simSolution1.Find("Structural")
        solutionResult1 = theSession.ResultManager.CreateReferenceResult(simResultReference1)
        
        # ----------------------------------------------
        #   Menu: Tools->Results->Color Display Type->Contour Plot
        # ----------------------------------------------
        postviewId1 = theSession.Post.CreateNewPostview(0, solutionResult1, False, NXOpen.CAE.Post.DisplayColorSchemeType.Fringe)
        
        # ----------------------------------------------
        #   Menu: Tools->Journal->Stop Recording
        # ----------------------------------------------
        
name = "partfemmesh26"
myduralok = Duralok(name, pipe_diam, lock_th)
myduralok.save_part()
myduralok.make_fem_model()
myduralok.do_sim()


"""
def getFaces(self):
    self.session  = NXOpen.Session.GetSession()
    #self.workPart = self.session.Parts.Work
    
    for partObject in self.session.Parts:
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