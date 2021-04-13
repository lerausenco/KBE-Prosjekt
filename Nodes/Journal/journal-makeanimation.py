# NX 1911
# Journal created by lera_ on Tue Apr 13 14:15:32 2021 W. Europe Summer Time
#
import math
import NXOpen
import NXOpen.CAE
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workSimPart = theSession.Parts.BaseWork
    displaySimPart = theSession.Parts.BaseDisplay
    # ----------------------------------------------
    #   Menu: File->Export->Animated GIF...
    # ----------------------------------------------
    # ----------------------------------------------
    #   Menu: Tools->Results->Animation...
    # ----------------------------------------------
    # ----------------------------------------------
    #   Menu: Tools->Results->Play
    # ----------------------------------------------
    theSession.Post.PostviewAnimationControl(1, NXOpen.CAE.Post.AnimationControl.Play, -1, True, -1)
    
    # ----------------------------------------------
    #   Menu: File->Export->Animated GIF...
    # ----------------------------------------------
    theSession.Post.PostviewCaptureAnimatedGif(1, "C:\\Users\\lera_\\OneDrive\\Dokumenter\\NTNU\\KBE\\KBE-Prosjekt\\Nodes\\Gif\\animation.gif", False, False)
    
    # ----------------------------------------------
    #   Menu: Tools->Results->Stop
    # ----------------------------------------------
    theSession.Post.PostviewAnimationControl(1, NXOpen.CAE.Post.AnimationControl.Stop, -1, True, -1)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()