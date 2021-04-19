# NX 1911
# Journal created by lera_ on Thu Apr 15 11:36:37 2021 W. Europe Summer Time
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
    
    unit1 = workSimPart.UnitCollection.FindObject("MilliMeter")
    expression1 = workSimPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    origin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
    vector1 = NXOpen.Vector3d(1.0, 0.0, 0.0)
    direction1 = workSimPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.AfterModeling)
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Force")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Force")
    
    objects1 = [None] * 1 
    objects1[0] = NXOpen.CAE.SetObject()
    component1 = workSimPart.ComponentAssembly.RootComponent.FindObject("COMPONENT fem_node231504210946_min 1")
    cAEFace1 = component1.FindObject("PROTO#CAE_Body(1)|CAE_Face(326)")
    objects1[0].Obj = cAEFace1
    objects1[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
    objects1[0].SubId = 0
    setManager1.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects1)
    
    unit2 = workSimPart.UnitCollection.FindObject("Newton")
    expression2 = workSimPart.Expressions.CreateSystemExpressionWithUnits("2000", unit2)
    
    fieldManager1 = workSimPart.FindObject("FieldManager")
    scalarFieldWrapper1 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression2)
    
    scalarFieldWrapper2 = propertyTable1.GetScalarFieldWrapperPropertyValue("TotalForce")
    
    expression3 = workSimPart.Expressions.CreateSystemExpressionWithUnits("2000", unit2)
    
    scalarFieldWrapper3 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression3)
    
    propertyTable1.SetScalarFieldWrapperPropertyValue("TotalForce", scalarFieldWrapper3)
    
    field1 = scalarFieldWrapper3.GetField()
    
    propertyTable1.SetVectorPropertyValue("Local Axis", direction1)
    
    propertyValue1 = []
    propertyTable1.SetTextPropertyValue("description", propertyValue1)
    
    simBCBuilder1.DestinationFolder = NXOpen.CAE.SimLbcFolder.Null
    
    simBC1 = simBCBuilder1.CommitAddBc()
    
    simBCBuilder1.Destroy()
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Force")
    
    workSimPart.Expressions.Delete(expression1)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()