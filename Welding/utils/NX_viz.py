from Shapes.Block import Block
import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities


f = open("C:/Users/lera_/OneDrive/Dokumenter/NTNU/KBE/KBE-Prosjekt/Welding/param_vals.txt", "r")

x_max = 0
y_max = 0

text = f.read()
#text = text.replace("(", "")
#text = text.replace(")", "")

lines = text.split("\n")
lines = lines[:-1]
num_lines = 0
for line in lines:
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace(" ", "")
    params = line.split(",") #x #y #width #height #wall height

    x = float(params[0])
    if x > x_max:
        x_max = x
    y = float(params[1] )
    if y > y_max:
        y_max = y
    width = float(params[2] )
    height = float(params[3] )
    wall_height = float(params[4])

    blockN = Block(x,y,0,width,height,wall_height)
    blockN.initForNX()
    num_lines+=1

bottom_plate = Block(0,0,-2,x_max, y_max, 2)
bottom_plate.initForNX()

theSession  = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work
displayPart = theSession.Parts.Display
# ----------------------------------------------
#   Menu: Insert->Combine->Unite...
# ----------------------------------------------
markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")

booleanBuilder1 = workPart.Features.CreateBooleanBuilderUsingCollector(NXOpen.Features.BooleanFeature.Null)

scCollector1 = booleanBuilder1.ToolBodyCollector

booleanRegionSelect1 = booleanBuilder1.BooleanRegionSelect

booleanBuilder1.Tolerance = 0.01

booleanBuilder1.Operation = NXOpen.Features.Feature.BooleanType.Unite

theSession.SetUndoMarkName(markId1, "Unite Dialog")

body1 = workPart.Bodies.FindObject("BLOCK("+str(num_lines+1)+")")
added1 = booleanBuilder1.Targets.Add(body1)

targets1 = [NXOpen.TaggedObject.Null] * 1 
targets1[0] = body1
booleanRegionSelect1.AssignTargets(targets1)

# ----------------------------------------------
#   Menu: Edit->Selection->Select All
# ----------------------------------------------
# Refer to the sample NXOpen application, Selection for "Select All" alternatives.
scCollector2 = workPart.ScCollectors.CreateCollector()

bodies1 = [NXOpen.Body.Null] * num_lines

for i in range(0,num_lines):
    bodyN = workPart.Bodies.FindObject("BLOCK("+str(i+1)+")")
    bodies1[i] = bodyN

bodyDumbRule1 = workPart.ScRuleFactory.CreateRuleBodyDumb(bodies1, True)
    
rules1 = [None] * 1 
rules1[0] = bodyDumbRule1
scCollector2.ReplaceRules(rules1, False)

booleanBuilder1.ToolBodyCollector = scCollector2

targets2 = [NXOpen.TaggedObject.Null] * 1 
targets2[0] = body1
booleanRegionSelect1.AssignTargets(targets2)

markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Unite")

theSession.DeleteUndoMark(markId2, None)

markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Unite")

nXObject1 = booleanBuilder1.Commit()

theSession.DeleteUndoMark(markId3, None)

theSession.SetUndoMarkName(markId1, "Unite")

booleanBuilder1.Destroy()

