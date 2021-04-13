# NX 1911
# Journal created by lera_ on Tue Apr 13 10:52:44 2021 W. Europe Summer Time
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
    
    part1 = theSession.Parts.FindObject("nicePart")
    femCreationOptions1.SetCadData(part1, "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Parts\\fem2_i1.prt")
    
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
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()