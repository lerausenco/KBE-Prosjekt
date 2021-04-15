import math
import NXOpen
import NXOpen.Annotations
import NXOpen.Features
import NXOpen.GeometricUtilities
import NXOpen.Preferences
class Cone:      
    
    def __init__(self,x, y, z, baseDiameter, topDiameter, height, direction, color, material):
        self.baseDiameter = baseDiameter    # instance variable unique to each instance
        self.topDiameter = topDiameter
        self.height = height
        self.direction = direction
        self.x = x    
        self.y = y
        self.z = z
        self.color = color
        self.material = material
        self.body = None
         
        
    def initForNX(self):
        theSession  = NXOpen.Session.GetSession()
        workPart = theSession.Parts.Work
        
        conebuilder1 = workPart.Features.CreateConeBuilder(NXOpen.Features.Cone.Null)
        conebuilder1.BaseDiameter.RightHandSide = str(self.baseDiameter) # Writing the right hand side of the expression
        conebuilder1.TopDiameter.RightHandSide = str(self.topDiameter)
        conebuilder1.Height.RightHandSide = str(self.height)
        centerPoint3D =  NXOpen.Point3d(float(self.x), float(self.y), float(self.z))
        centerPoint = workPart.Points.CreatePoint(centerPoint3D)
        conebuilder1.Axis.Point = centerPoint
        vector3D_ = NXOpen.Vector3d(float(self.direction[0]),float(self.direction[1]),float(self.direction[2]))
    
        # Setting direction of the Cone
        conebuilder1.Axis.Direction.Vector = vector3D_
    
        conebuilder1.BooleanOption.Type = NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create

        self.body = conebuilder1.CommitFeature().GetBodies()[0]
        conebuilder1.Destroy()
        return self.body
        
    def subtract(self, tool):
        theSession  = NXOpen.Session.GetSession()
        workPart = theSession.Parts.Work

        # Subtraction
        subtractfeaturebuilder1 = workPart.Features.CreateBooleanBuilder(NXOpen.Features.BooleanFeature.Null)
        
        subtractfeaturebuilder1.Target = self.body # From where to subtract
        subtractfeaturebuilder1.Tool = tool.body # What to subtract
        subtractfeaturebuilder1.Operation = NXOpen.Features.FeatureBooleanType.Subtract
        
        subtractfeaturebuilder1.Commit()
        subtractfeaturebuilder1.Destroy()



