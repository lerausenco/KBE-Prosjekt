﻿# NX 1911
# Journal created by lera_ on Thu Apr 15 10:14:14 2021 W. Europe Summer Time
#
import math
import NXOpen
import NXOpen.Assemblies
import NXOpen.CAE
import NXOpen.Fields
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workSimPart = theSession.Parts.BaseWork
    displaySimPart = theSession.Parts.BaseDisplay
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    simPart1 = workSimPart
    simSimulation1 = simPart1.Simulation
    
    simBCBuilder1 = simSimulation1.CreateBcBuilderForLoadDescriptor("magnitudeDirectionForce", "Force(3)", 3)
    
    propertyTable1 = simBCBuilder1.PropertyTable
    
    setManager1 = simBCBuilder1.TargetSetManager
    
    theSession.SetUndoMarkName(markId1, "Force Dialog")
    
    # ----------------------------------------------
    #   Dialog Begin Force
    # ----------------------------------------------
    unit1 = workSimPart.UnitCollection.FindObject("MilliMeter")
    expression1 = workSimPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    origin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
    vector1 = NXOpen.Vector3d(-0.0, -0.0, -1.0)
    direction1 = workSimPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.AfterModeling)
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Force")
    
    objects1 = [None] * 1 
    objects1[0] = NXOpen.CAE.SetObject()
    component1 = workSimPart.ComponentAssembly.RootComponent.FindObject("COMPONENT fem_node11504210946 1")
    cAEFace1 = component1.FindObject("PROTO#CAE_Body(1)|CAE_Face(45)")
    objects1[0].Obj = cAEFace1
    objects1[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
    objects1[0].SubId = 0
    setManager1.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects1)
    
    unit2 = workSimPart.UnitCollection.FindObject("Newton")
    expression2 = workSimPart.Expressions.CreateSystemExpressionWithUnits("1234", unit2)
    
    fieldManager1 = workSimPart.FindObject("FieldManager")
    scalarFieldWrapper1 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression2)
    
    scalarFieldWrapper2 = propertyTable1.GetScalarFieldWrapperPropertyValue("TotalForce")
    
    expression3 = workSimPart.Expressions.CreateSystemExpressionWithUnits("1234", unit2)
    
    scalarFieldWrapper3 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression3)
    
    propertyTable1.SetScalarFieldWrapperPropertyValue("TotalForce", scalarFieldWrapper3)
    
    field1 = scalarFieldWrapper3.GetField()
    
    propertyTable1.SetVectorPropertyValue("Local Axis", direction1)
    
    propertyValue1 = []
    propertyTable1.SetTextPropertyValue("description", propertyValue1)
    
    simBCBuilder1.DestinationFolder = NXOpen.CAE.SimLbcFolder.Null
    
    simBC1 = simBCBuilder1.CommitAddBc()
    
    simBCBuilder1.Destroy()
    
    theSession.DeleteUndoMark(markId2, None)
    
    theSession.SetUndoMarkName(markId1, "Force")
    
    workSimPart.Expressions.Delete(expression1)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    simPart2 = workSimPart
    simSimulation2 = simPart2.Simulation
    
    simBCBuilder2 = simSimulation2.CreateBcBuilderForLoadDescriptor("magnitudeDirectionForce", "Force(4)", 4)
    
    propertyTable2 = simBCBuilder2.PropertyTable
    
    setManager2 = simBCBuilder2.TargetSetManager
    
    theSession.SetUndoMarkName(markId3, "Force Dialog")
    
    # ----------------------------------------------
    #   Dialog Begin Force
    # ----------------------------------------------
    simBCBuilder2.Destroy()
    
    theSession.UndoToMark(markId3, None)
    
    theSession.DeleteUndoMark(markId3, None)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()