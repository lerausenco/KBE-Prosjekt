# NX 1911
# Journal created by lera_ on Tue Apr 13 12:02:27 2021 W. Europe Summer Time
#
import math
import NXOpen
import NXOpen.Assemblies
import NXOpen.CAE
import NXOpen.Fields
import NXOpen.MenuBar
import NXOpen.PhysMat
def main() : 

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
    femPart1 = theSession.Parts.FindObject("fem_partfemmesh20")
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
    component1 = workSimPart.ComponentAssembly.RootComponent.FindObject("COMPONENT fem_partfemmesh20 1")
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
    
    simResultReference1 = simSolution1.Find("Structural")
    solutionResult1 = theSession.ResultManager.CreateReferenceResult(simResultReference1)
    
    # ----------------------------------------------
    #   Menu: Tools->Results->Color Display Type->Contour Plot
    # ----------------------------------------------
    postviewId1 = theSession.Post.CreateNewPostview(0, solutionResult1, False, NXOpen.CAE.Post.DisplayColorSchemeType.Fringe)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()