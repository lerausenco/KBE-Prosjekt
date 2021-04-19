# NX 1911
# Journal created by lera_ on Thu Apr 15 11:15:18 2021 W. Europe Summer Time
#
import math
import NXOpen
import NXOpen.CAE
import NXOpen.MenuBar
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workSimPart = theSession.Parts.BaseWork
    displaySimPart = theSession.Parts.BaseDisplay
    simPart1 = workSimPart
    theSession.Post.PostviewDelete(1)
    
    simPart1.Close(NXOpen.BasePart.CloseWholeTree.TrueValue, NXOpen.BasePart.CloseModified.UseResponses, None)
    
    workSimPart = NXOpen.BasePart.Null
    displaySimPart = NXOpen.BasePart.Null
    theSession.ApplicationSwitchImmediate("UG_APP_NOPART")
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()