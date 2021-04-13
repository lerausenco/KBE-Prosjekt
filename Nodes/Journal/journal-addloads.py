# NX 1911
# Journal created by lera_ on Tue Apr 13 11:34:02 2021 W. Europe Summer Time
#
import math
import NXOpen
import NXOpen.CAE
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
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()