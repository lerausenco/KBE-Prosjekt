# NX 1911
# Journal created by lera_ on Tue Apr 13 10:57:17 2021 W. Europe Summer Time
#
import math
import NXOpen
import NXOpen.CAE
import NXOpen.MenuBar
def main() : 

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
    
    fileNew1.NewFileName = "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\fem2.fem"
    
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
    
    part1 = theSession.Parts.FindObject("femmypart")
    femCreationOptions1.SetCadData(part1, "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\fem2_i2.prt")
    
    bodies1 = [NXOpen.Body.Null] * 1 
    body1 = part1.Bodies.FindObject("CONE(1)")
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
    
    # ----------------------------------------------
    #   Menu: Insert->Mesh->3D Tetrahedral Mesh...
    # ----------------------------------------------
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
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()