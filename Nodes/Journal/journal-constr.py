# NX 1911
# Journal created by lera_ on Thu Apr 15 11:07:35 2021 W. Europe Summer Time
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
    
    simBCBuilder1 = simSimulation1.CreateBcBuilderForConstraintDescriptor("fixedConstraint", "Fixed(2)", 2)
    
    propertyTable1 = simBCBuilder1.PropertyTable
    
    setManager1 = simBCBuilder1.TargetSetManager
    
    fieldExpression1 = propertyTable1.GetScalarFieldPropertyValue("DOF1")
    
    fieldExpression2 = propertyTable1.GetScalarFieldPropertyValue("DOF2")
    
    fieldExpression3 = propertyTable1.GetScalarFieldPropertyValue("DOF3")
    
    fieldExpression4 = propertyTable1.GetScalarFieldPropertyValue("DOF4")
    
    fieldExpression5 = propertyTable1.GetScalarFieldPropertyValue("DOF5")
    
    fieldExpression6 = propertyTable1.GetScalarFieldPropertyValue("DOF6")
    
    theSession.SetUndoMarkName(markId1, "Fixed Constraint Dialog")
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Fixed Constraint")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Fixed Constraint")
    
    objects1 = [None] * 1 
    objects1[0] = NXOpen.CAE.SetObject()
    component1 = workSimPart.ComponentAssembly.RootComponent.FindObject("COMPONENT fem_node161504210946_min 1")
    cAEFace1 = component1.FindObject("PROTO#CAE_Body(1)|CAE_Face(16)")
    objects1[0].Obj = cAEFace1
    objects1[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
    objects1[0].SubId = 0
    setManager1.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects1)
    
    unit1 = workSimPart.UnitCollection.FindObject("MilliMeter")
    indepVarArray1 = []
    fieldExpression1.EditFieldExpression("0", unit1, indepVarArray1, False)
    
    propertyTable1.SetScalarFieldPropertyValue("DOF1", fieldExpression1)
    
    indepVarArray2 = []
    fieldExpression2.EditFieldExpression("0", unit1, indepVarArray2, False)
    
    propertyTable1.SetScalarFieldPropertyValue("DOF2", fieldExpression2)
    
    indepVarArray3 = []
    fieldExpression3.EditFieldExpression("0", unit1, indepVarArray3, False)
    
    propertyTable1.SetScalarFieldPropertyValue("DOF3", fieldExpression3)
    
    unit2 = workSimPart.UnitCollection.FindObject("Degrees")
    indepVarArray4 = []
    fieldExpression4.EditFieldExpression("0", unit2, indepVarArray4, False)
    
    propertyTable1.SetScalarFieldPropertyValue("DOF4", fieldExpression4)
    
    indepVarArray5 = []
    fieldExpression5.EditFieldExpression("0", unit2, indepVarArray5, False)
    
    propertyTable1.SetScalarFieldPropertyValue("DOF5", fieldExpression5)
    
    indepVarArray6 = []
    fieldExpression6.EditFieldExpression("0", unit2, indepVarArray6, False)
    
    propertyTable1.SetScalarFieldPropertyValue("DOF6", fieldExpression6)
    
    propertyValue1 = []
    propertyTable1.SetTextPropertyValue("description", propertyValue1)
    
    simBCBuilder1.DestinationFolder = NXOpen.CAE.SimLbcFolder.Null
    
    simBC1 = simBCBuilder1.CommitAddBc()
    
    simBCBuilder1.Destroy()
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Fixed Constraint")
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()