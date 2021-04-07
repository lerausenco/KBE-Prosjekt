import math
import NXOpen
import NXOpen.Annotations
import NXOpen.Features
import NXOpen.GeometricUtilities
import NXOpen.Preferences
class Sphere:
	
	def getVolume(self):
		return 4/3 * 3.14 * self.diameter/2 * self.diameter/2 * self.diameter/2
    
	def __init__(self, x, y, z, diameter, color, material):
		self.diameter = diameter    # instance variable unique to each instance
		self.x = x    
		self.y = y
		self.z = z
		self.color = color
		self.material = material
		self.body = None
		 
		
	def initForNX(self):
		theSession  = NXOpen.Session.GetSession()
		workPart = theSession.Parts.Work
		
		spherebuilder1 = workPart.Features.CreateSphereBuilder(NXOpen.Features.Sphere.Null)

		spherebuilder1.Diameter.RightHandSide = str(self.diameter) # Writing the right hand side of the expression
		centerPoint3D =  NXOpen.Point3d(float(self.x), float(self.y), float(self.z))
		centerPoint = workPart.Points.CreatePoint(centerPoint3D)
		spherebuilder1.CenterPoint = centerPoint 
		spherebuilder1.BooleanOption.Type = NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create

		self.body = spherebuilder1.CommitFeature().GetBodies()[0]
		spherebuilder1.Destroy()
		
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