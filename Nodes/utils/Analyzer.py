import math
import random
import NXOpen
import NXOpen.Assemblies
import NXOpen.CAE
import NXOpen.Fields
import NXOpen.PhysMat

class Analyzer:

	"""
	Constructor for the Analyzer class. Gets filename and filepath as input parameters.
	These does not have to be the actual files, as the model can be constructed from 
	and with NX Open API.
	"""
	def __init__(self, filename, filepath):
		print("Analyzer has started.")
		self.fileName = filename + str(random.randint(1, 1000000)) # To allow several sessions to run smoothly without collisions between "files"
		self.filePath = filepath
		# Bodies to analyze - to be updated via getSolidBodies method.
		self.bodies = []
	
	def getSolidBodies(self):
		theSession  = NXOpen.Session.GetSession()
		try:
			workPart = theSession.Parts.Work

		#just a check to see if parts can be created in FEM mode. It's possible, but they need to be loaded into the correct environment
		except Exception as e:
			workPart = theSession.Parts.BaseWork

		#object for showing dialogue boxes
		theNxMessageBox = NXOpen.UI.GetUI().NXMessageBox

		#collect all objects on a particular layer (default is 1)
		objects = workPart.Layers.GetAllObjectsOnLayer(1)

		body_counter = 0
		face_counter = 0
		#Loops through all objects
		for object in objects:
			try:
				#attempts to check if object is a body
				if object.IsSolidBody:

					body_counter += 1
					self.bodies.append(object)

					#if object is a body, collect all faces
					faces = object.GetFaces()

					face_counter += len(faces)


			#if error is met, do nothing
			except Exception as e:
				pass

		#theNxMessageBox.Show("Total objects",NXOpen.NXMessageBoxDialogType.Information, str(len(objects)))
		theNxMessageBox.Show("Bodies",NXOpen.NXMessageBoxDialogType.Information, str(body_counter))
		
		# Loop through the bodies and display their names / journal indentifiers
		for body in self.bodies:
			theNxMessageBox.Show("Body name",NXOpen.NXMessageBoxDialogType.Information, str(body.JournalIdentifier))
		
		theNxMessageBox.Show("Faces count",NXOpen.NXMessageBoxDialogType.Information, str(face_counter))
	
	"""
	Creates FEM
	
	Parameters:
	
	meshMaxVal - quad mesh overall edge size.
	meshMinVal - small feature value.
	material - The material the part is made of, e.g. "Aluminum_5086".
	
	"""
	def createFEM(self, meshMaxVal, meshMinVal, material):
		theSession  = NXOpen.Session.GetSession()
		workPart = theSession.Parts.Work
		part1 = workPart # Why not?
		
		#theNxMessageBox = NXOpen.UI.GetUI().NXMessageBox
		#theNxMessageBox.Show("Bodies count",NXOpen.NXMessageBoxDialogType.Information, str(len(self.bodies)))
		
		femFile = theSession.Parts.FileNew()
		femFile.TemplateFileName = "FemNxNastranMetric.fem"
		femFile.UseBlankTemplate = False
		femFile.ApplicationName = "CaeFemTemplate"
		femFile.Units = NXOpen.Part.Units.Millimeters
		femFile.RelationType = ""
		femFile.UsesMasterModel = "No"
		femFile.TemplateType = NXOpen.FileNewTemplateType.Item
		femFile.TemplatePresentationName = "NX Nastran"
		femFile.ItemType = ""
		femFile.Specialization = ""
		femFile.SetCanCreateAltrep(False)
		femFile.NewFileName = self.filePath + self.fileName + ".fem"
		femFile.MasterFileName = ""
		femFile.MakeDisplayedPart = True
		femFile.DisplayPartOption = NXOpen.DisplayPartOption.AllowAdditional
		
		baseTemplateManager1 = theSession.XYPlotManager.TemplateManager
		
		#nXObject1 = femFile.Commit()
		
		workPart = NXOpen.Part.Null
		workFemPart = theSession.Parts.BaseWork
		
		#Test
		#for obj in workFemPart.Layers.GetAllObjectsOnLayer(1):
		#	theNxMessageBox.Show("WFP object name",NXOpen.NXMessageBoxDialogType.Information, str(obj.JournalIdentifier))
		
		
		displayPart = NXOpen.Part.Null
		displayFemPart = theSession.Parts.BaseDisplay
		
		femFile.Destroy()
		
		femPart1 = workFemPart
		femPart1.PolygonGeometryMgr.SetPolygonBodyResolutionOnFemBodies(NXOpen.CAE.PolygonGeometryManager.PolygonBodyResolutionType.Standard)
		femPart2 = workFemPart
		femCreationOptions1 = femPart2.NewFemCreationOptions()
		femPart3 = workFemPart
		femSynchronizeOptions1 = femPart3.NewFemSynchronizeOptions()
		
		femSynchronizeOptions1.SynchronizePointsFlag = False
		femSynchronizeOptions1.SynchronizeCoordinateSystemFlag = False
		femSynchronizeOptions1.SynchronizeLinesFlag = False
		femSynchronizeOptions1.SynchronizeArcsFlag = False
		femSynchronizeOptions1.SynchronizeSplinesFlag = False
		femSynchronizeOptions1.SynchronizeConicsFlag = False
		femSynchronizeOptions1.SynchronizeSketchCurvesFlag = False
		
		#part1 = workPart #theSession.Parts.FindObject("model7")
		# NB! -----> workPart / set in the beginning of the method
		femCreationOptions1.SetCadData(part1, self.filePath + self.fileName + "_i.prt") #NB!
		
			
		bodies1 = [NXOpen.Body.Null] * 1 
		body1 = part1.Bodies.FindObject(str(self.bodies[0].JournalIdentifier)) #Refers to the object - TODO the search
		bodies1[0] = body1
		femCreationOptions1.SetGeometryOptions(NXOpen.CAE.FemCreationOptions.UseBodiesOption.VisibleBodies, bodies1, femSynchronizeOptions1)
		femCreationOptions1.SetSolverOptions("NX NASTRAN", "Structural", NXOpen.CAE.BaseFemPart.AxisymAbstractionType.NotSet)
		
		description1 = []
		femCreationOptions1.SetDescription(description1)
		
		femCreationOptions1.SetMorphingFlag(False)
		femCreationOptions1.SetCyclicSymmetryData(False, NXOpen.CoordinateSystem.Null)
		
		femPart4 = workFemPart
		femPart4.FinalizeCreation(femCreationOptions1)
		
		femSynchronizeOptions1.Dispose()
		femCreationOptions1.Dispose()
		
		theSession.ApplicationSwitchImmediate("UG_APP_SFEM")
		#+
		# ----------------------------------------------
		#   Switch to Design Simulation
		# ----------------------------------------------
		theSession.ApplicationSwitchImmediate("UG_APP_DESFEM")
		
		# ----------------------------------------------
		#   Assign Materials...
		# ----------------------------------------------
		physicalMaterialListBuilder1 = workFemPart.MaterialManager.PhysicalMaterials.CreateListBlockBuilder()
		physicalMaterialAssignBuilder1 = workFemPart.MaterialManager.PhysicalMaterials.CreateMaterialAssignBuilder()   	
		physicalMaterial1 = workFemPart.MaterialManager.PhysicalMaterials.LoadFromNxmatmllibrary(material)
		
		objects1 = [NXOpen.NXObject.Null] * 1
		cAEBody1 = workFemPart.FindObject("CAE_Body(1)")
		objects1[0] = cAEBody1
		physicalMaterial1.AssignObjects(objects1)
		
		physicalMaterialAssignBuilder1.Destroy()
		physicalMaterialListBuilder1.Destroy()
		
		# ** 3
		
		fEModel1 = workFemPart.FindObject("FEModel")
		meshManager1 = fEModel1.Find("MeshManager")
		mesh3dTetBuilder1 = meshManager1.CreateMesh3dTetBuilder(NXOpen.CAE.Mesh3d.Null)
		
		mesh3dTetBuilder1.ElementType.DestinationCollector.ElementContainer = NXOpen.CAE.MeshCollector.Null
		mesh3dTetBuilder1.ElementType.ElementTypeName = "CTETRA(10)"
		unit1 = workFemPart.UnitCollection.FindObject("MilliMeter")

		added1 = mesh3dTetBuilder1.SelectionList.Add(cAEBody1)
		
		mesh3dTetBuilder1.AutoResetOption = False
		mesh3dTetBuilder1.ElementType.ElementDimension = NXOpen.CAE.ElementTypeBuilder.ElementType.FreeSolid
		mesh3dTetBuilder1.ElementType.ElementTypeName = "CTETRA(10)"
		destinationCollectorBuilder1 = mesh3dTetBuilder1.ElementType.DestinationCollector		
		destinationCollectorBuilder1.ElementContainer = NXOpen.CAE.MeshCollector.Null
		destinationCollectorBuilder1.AutomaticMode = True
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh overall edge size", meshMaxVal, unit1)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("mapped mesh option bool", True)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("multiblock cylinder option bool", False)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("fillet num elements", 3)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("num elements on cylinder circumference", 6)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("element size on cylinder height", "1", unit1)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("create pyramids bool", False)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("midnodes", 0)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("geometry tolerance option bool", False)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("geometry tolerance", "0", unit1)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("max jacobian", "10", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("surface mesh size variation", "50", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("volume mesh size variation", "50", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("internal mesh gradation", "1.05", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("internal max edge option bool", False)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("internal max edge length value", "0", unit1)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("two elements through thickness bool", False)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("mesh transition bool", False)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("remesh on bad quality bool", False)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("maximum edge length bool", False)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("maximum edge length", "1", unit1)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("small feature tolerance", "10", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("small feature value", meshMinVal, NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("boundary layer element type", 3)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("insert blend elements", True)
		
		unit2 = workFemPart.UnitCollection.FindObject("Degrees")
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("blending angle", "90", unit2)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("sweep angle", "45", unit2)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("control aspect ratio", False)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("maximum exposed aspect ratio", "1000", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("control slender", False)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("minimum aspect ratio", "0.01", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("maximum imprint dihedral angle", "120", unit2)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("gradation rate", "10", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("smoothing distance factor", "3", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBooleanPropertyValue("all-tet boundary layer", False)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("dont format mesh to solver", 0)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh edge match tolerance", "0.02", NXOpen.Unit.Null)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh smoothness tolerance", "0.01", unit1)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("min face angle", "20", unit2)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("mesh time stamp", 0)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("quad mesh node coincidence tolerance", "0.0001", unit1)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("mesh edit allowed", 0)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("edge angle", "15", unit2)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("merge edge toggle", 0)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("auto constraining", 1)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("curvature scaling", 1)
		mesh3dTetBuilder1.PropertyTable.SetBaseScalarWithDataPropertyValue("target angle", "45", unit2)
		mesh3dTetBuilder1.PropertyTable.SetIntegerPropertyValue("edge shape", 2)
		
		
		meshes1 = mesh3dTetBuilder1.CommitMesh()
		
		mesh3dTetBuilder1.Destroy()
		
	"""
	To do as an idependent method ? 
	"""	
	def assignMaterial(self):
		pass
	
	"""
	Defines the simulation
	"""
	def defineSim(self):
		filename = self.fileName

		theSession  = NXOpen.Session.GetSession()
		workFemPart = theSession.Parts.BaseWork
		displayFemPart = theSession.Parts.BaseDisplay

		simFile = theSession.Parts.FileNew()
		simFile.TemplateFileName = "SimNxNastranMetric.sim"
		simFile.UseBlankTemplate = False
		simFile.ApplicationName = "CaeSimTemplate"
		simFile.Units = NXOpen.Part.Units.Millimeters
		simFile.RelationType = ""
		simFile.UsesMasterModel = "No"
		simFile.TemplateType = NXOpen.FileNewTemplateType.Item
		simFile.TemplatePresentationName = "NX Nastran"
		simFile.ItemType = ""
		simFile.Specialization = ""
		simFile.SetCanCreateAltrep(False)

		simFile.NewFileName = self.filePath + self.fileName + "_fem_sim1.sim"
		simFile.MasterFileName = ""
		simFile.MakeDisplayedPart = True
		simFile.DisplayPartOption = NXOpen.DisplayPartOption.AllowAdditional

		baseTemplateManager1 = theSession.XYPlotManager.TemplateManager
		nXObject1 = simFile.Commit()
		workSimPart = theSession.Parts.BaseWork
		displaySimPart = theSession.Parts.BaseDisplay

		simPart1 = workSimPart
		femPart1 = theSession.Parts.FindObject(filename) # + '_fem')
		description1 = []
		simPart1.FinalizeCreation(femPart1, 0, description1)
		simFile.Destroy()
		simPart2 = workSimPart
		simSimulation1 = simPart2.Simulation
		simSolution1 = simSimulation1.CreateSolution("NX NASTRAN", "Structural", "SESTATIC 101 - Single Constraint", "Solution 1", NXOpen.CAE.SimSimulation.AxisymAbstractionType.NotSet)
		propertyTable1 = simSolution1.PropertyTable
		caePart1 = workSimPart
		modelingObjectPropertyTable1 = caePart1.ModelingObjectPropertyTables.CreateModelingObjectPropertyTable("Bulk Data Echo Request", "NX NASTRAN - Structural", "NX NASTRAN", "Bulk Data Echo Request1", 1)
		caePart2 = workSimPart
		modelingObjectPropertyTable2 = caePart2.ModelingObjectPropertyTables.CreateModelingObjectPropertyTable("Structural Output Requests", "NX NASTRAN - Structural", "NX NASTRAN", "Structural Output Requests1", 2)
		simSolution1.Rename("Solution 1", False)
		propertyTable2 = simSolution1.PropertyTable
		propertyTable2.SetNamedPropertyTablePropertyValue("Bulk Data Echo Request", modelingObjectPropertyTable1)
		propertyTable2.SetNamedPropertyTablePropertyValue("Output Requests", modelingObjectPropertyTable2)
		simSolutionStep1 = simSolution1.CreateStep(0, True, "Subcase - Static Loads 1")

	"""
	Assignes fixed constrain for given body and its face 
	"""
	def assignConstrain(self, body, face):
		theSession  = NXOpen.Session.GetSession()
		workSimPart = theSession.Parts.BaseWork

		simPart1 = workSimPart
		simSimulation1 = simPart1.Simulation

		#Applying the constraint
		simBCBuilder1 = simSimulation1.CreateBcBuilderForConstraintDescriptor("fixedConstraint", "Fixed(1)", 1)
		propertyTable1 = simBCBuilder1.PropertyTable
		setManager1 = simBCBuilder1.TargetSetManager

		objects1 = [None] * 1
		objects1[0] = NXOpen.CAE.SetObject()
		component1 = workSimPart.ComponentAssembly.RootComponent.FindObject("COMPONENT " + self.fileName + " 1") # "_fem 1")
		cAEFace1 = component1.FindObject("PROTO#CAE_Body(" + str(body) + ")|CAE_Face(" + str(face) + ")")
		objects1[0].Obj = cAEFace1
		objects1[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
		objects1[0].SubId = 0
		setManager1.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects1)

		#translational motion constraint
		unit_tran = workSimPart.UnitCollection.FindObject("MilliMeter")
		indepVarArray = []
		fieldExpression1 = propertyTable1.GetScalarFieldPropertyValue("DOF1")
		fieldExpression1.EditFieldExpression("0", unit_tran, indepVarArray, False)
		propertyTable1.SetScalarFieldPropertyValue("DOF1", fieldExpression1)
		propertyTable1.SetScalarFieldPropertyValue("DOF2", fieldExpression1)
		propertyTable1.SetScalarFieldPropertyValue("DOF3", fieldExpression1)

		#rotational motion constraint
		unit_deg = workSimPart.UnitCollection.FindObject("Degrees")
		fieldExpression4 = propertyTable1.GetScalarFieldPropertyValue("DOF4")
		fieldExpression4.EditFieldExpression("0", unit_deg, indepVarArray, False)
		propertyTable1.SetScalarFieldPropertyValue("DOF4", fieldExpression4)
		propertyTable1.SetScalarFieldPropertyValue("DOF5", fieldExpression4)
		propertyTable1.SetScalarFieldPropertyValue("DOF6", fieldExpression4)

		simBC1 = simBCBuilder1.CommitAddBc()
		
	"""
	Defines the load (force) acting on given body's face in the given direction 
	"""
	def assignLoad(self, force, body, face, direction):
		theSession  = NXOpen.Session.GetSession()
		workSimPart = theSession.Parts.BaseWork
		simSimulation1 = workSimPart.Simulation

		simBCBuilder2 = simSimulation1.CreateBcBuilderForLoadDescriptor("magnitudeDirectionForce", "Force(1)", 1)

		propertyTable2 = simBCBuilder2.PropertyTable

		setManager2 = simBCBuilder2.TargetSetManager

		objects2 = [None] * 1
		objects2[0] = NXOpen.CAE.SetObject()
		component1 = workSimPart.ComponentAssembly.RootComponent.FindObject("COMPONENT " + self.fileName + " 1") # "_fem 1")

		#Can be used with the find all objects function
		#In theory, more faces could be added at once? For us it's probably easier to loop through this function at the higher level
		cAEFace2 = component1.FindObject("PROTO#CAE_Body(" + str(body) + ")|CAE_Face(" + str(face) + ")")
		objects2[0].Obj = cAEFace2
		objects2[0].SubType = NXOpen.CAE.CaeSetObjectSubType.NotSet
		objects2[0].SubId = 0
		setManager2.SetTargetSetMembers(0, NXOpen.CAE.CaeSetGroupFilterType.GeomFace, objects2)

		unit_force = workSimPart.UnitCollection.FindObject("Newton")
		expression2 = workSimPart.Expressions.CreateSystemExpressionWithUnits(str(force), unit_force)

		fieldManager1 = workSimPart.FindObject("FieldManager")
		scalarFieldWrapper1 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression2)
		scalarFieldWrapper2 = propertyTable2.GetScalarFieldWrapperPropertyValue("TotalForce")
		scalarFieldWrapper3 = fieldManager1.CreateScalarFieldWrapperWithExpression(expression2)


		origin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
		vector1 = NXOpen.Vector3d(float(direction[0]), float(direction[1]), float(direction[2]))
		direction1 = workSimPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.AfterModeling)

		propertyTable2.SetScalarFieldWrapperPropertyValue("TotalForce", scalarFieldWrapper3)
		propertyTable2.SetVectorPropertyValue("Local Axis", direction1)

		simBC2 = simBCBuilder2.CommitAddBc()
		
	"""
	Solves the simulation...
	"""
	def solveSim(self):
		theSession  = NXOpen.Session.GetSession()
		workSimPart = theSession.Parts.BaseWork
		displaySimPart = theSession.Parts.BaseDisplay

		theSimSolveManager = NXOpen.CAE.SimSolveManager.GetSimSolveManager(theSession)

		simSimulation1 = workSimPart.FindObject("Simulation")
		simSolution1 = simSimulation1.FindObject("Solution[Solution 1]")
		psolutions1 = [NXOpen.CAE.SimSolution.Null] * 1
		psolutions1[0] = simSolution1
		numsolutionssolved1, numsolutionsfailed1, numsolutionsskipped1 = theSimSolveManager.SolveChainOfSolutions(psolutions1, NXOpen.CAE.SimSolution.SolveOption.Solve, NXOpen.CAE.SimSolution.SetupCheckOption.CompleteCheckAndOutputErrors, NXOpen.CAE.SimSolution.SolveMode.Background)
	"""
	Review the results
	"""
	def openResults(self):
		theSession  = NXOpen.Session.GetSession()
		workSimPart = theSession.Parts.BaseWork
		displaySimPart = theSession.Parts.BaseDisplay
		simSimulation1 = workSimPart.FindObject("Simulation")
		simSolution1 = simSimulation1.FindObject("Solution[Solution 1]")
		simResultReference1 = simSolution1.Find("Structural")
		solutionResult1 = theSession.ResultManager.CreateReferenceResult(simResultReference1)
		
		resultParameters1 = theSession.ResultManager.CreateResultParameters()
		resultParameters1.SetDBScaling(0)
		signalProcessingDBSettings1 = resultParameters1.GetDbSettings()
		
		loadcase1 = solutionResult1.Find("Loadcase[1]")
		iteration1 = loadcase1.Find("Iteration[1]")
		resultType1 = iteration1.Find("ResultType[[Displacement][Nodal]]")
		resultParameters1.SetGenericResultType(resultType1)
		
		resultParameters1.SetResultBeamSection(NXOpen.CAE.Result.Section.ValueOf(-1))
		resultParameters1.SetResultShellSection(NXOpen.CAE.Result.Section.ValueOf(-1))
		resultParameters1.SetResultComponent(NXOpen.CAE.Result.Component.ValueOf(-1))
		resultParameters1.SetCoordinateSystem(NXOpen.CAE.Result.CoordinateSystem.AbsoluteRectangular)
		resultParameters1.SetSelectedCoordinateSystem(NXOpen.CAE.Result.CoordinateSystemSource.NotSet, -1)
		
		resultParameters1.SetRotationAxisOfAbsoluteCyndricalCSYS(NXOpen.CAE.Post.AxisymetricAxis.X)
		
		resultParameters1.SetBeamResultsInLocalCoordinateSystem(True)
		
		resultParameters1.MakeElementResult(False)
		
		resultParameters1.SetElementValueCriterion(NXOpen.CAE.Result.ElementValueCriterion.Average)
		
		average1 = NXOpen.CAE.Result.Averaging()
		
		average1.DoAveraging = False
		average1.AverageAcrossPropertyIds = True
		average1.AverageAcrossMaterialIds = True
		average1.AverageAcrossElementTypes = True
		average1.AverageAcrossFeatangle = True
		average1.AverageAcrossAnglevalue = 45.0
		average1.IncludeInternalElementContributions = True
		resultParameters1.SetAveragingCriteria(average1)
		
		resultParameters1.SetComputationType(NXOpen.CAE.Result.ComputationType.NotSet)
		
		resultParameters1.SetComputeOnVisible(False)
		
		resultParameters1.SetComplexCriterion(NXOpen.CAE.Result.Complex.Amplitude)
		
		resultParameters1.SetPhaseAngle(0.0)
		
		resultParameters1.SetSectionPlyLayer(0, 0, 1)
		
		resultParameters1.SetScale(1.0)
		
		unit1 = workSimPart.UnitCollection.FindObject("MilliMeter")
		resultParameters1.SetUnit(unit1)
		
		resultParameters1.SetAbsoluteValue(False)
		
		resultParameters1.SetTensorComponentAbsoluteValue(NXOpen.CAE.Result.TensorDerivedAbsolute.DerivedComponent)
		
		resultParameters1.SetCalculateBeamStrResults(False)
		
		resultParameters1.SetBeamFillets(True)
		
		resultParameters1.SetBeamFilletRadius(0.5)
		
		resultParameters1.DisplayMidnodeValue(True)
		
		resultParameters1.SetIsReferenceNode(False)
		
		resultParameters1.SetReferenceNodeLabel(0)
		
		cyclicSymmetricParameters1 = resultParameters1.GetCyclicSymmetricParameters()
		
		cyclicSymmetricParameters1.ResultOption = NXOpen.CAE.CyclicSymmetricParameters.GetResult.OnOriginalModel
		
		cyclicSymmetricParameters1.OriginalResultOption = NXOpen.CAE.CyclicSymmetricParameters.OriginalResult.BySector
		
		cyclicSymmetricParameters1.SectCriteria = NXOpen.CAE.CyclicSymmetricParameters.SectorCriteria.Index
		
		cyclicSymmetricParameters1.SectorValue = NXOpen.CAE.CyclicSymmetricParameters.Value.Maximum
		
		cyclicSymmetricParameters1.EnvValue = NXOpen.CAE.CyclicSymmetricParameters.EnvelopeValue.Average
		
		cyclicSymmetricParameters1.SectorIndex = 1
		
		sectors1 = []
		cyclicSymmetricParameters1.SetSectorIndices(sectors1)
		
		axiSymmetricParameters1 = resultParameters1.GetAxiSymmetricParameters()
		
		axiSymmetricParameters1.ResultOption = NXOpen.CAE.AxiSymmetricParameters.GetResult.OnOriginalModel
		
		axiSymmetricParameters1.RotationAxis = NXOpen.CAE.AxiSymmetricParameters.AxisOfRotation.XAxis
		
		axiSymmetricParameters1.AxiOptions = NXOpen.CAE.AxiSymmetricParameters.Options.AtRevolveAngle
		
		axiSymmetricParameters1.EnvelopeVal = NXOpen.CAE.AxiSymmetricParameters.EnvVal.Average
		
		axiSymmetricParameters1.RevolveAngle = 0.0
		
		axiSymmetricParameters1.StartRevolveAngle = 0.0
		
		axiSymmetricParameters1.EndRevolveAngle = 360.0
		
		axiSymmetricParameters1.NumberOfSections = 40
		
		postviewId1 = theSession.Post.CreatePostviewForResult(0, solutionResult1, False, resultParameters1)
		theSession.ResultManager.DeleteResultParameters(resultParameters1)
		
	"""
	Runs animation
	"""
	def runAnimation(self):
		theSession = NXOpen.Session.GetSession()
		animation1 = NXOpen.CAE.Post.AnimationParameters()
	
		animation1.AnimationType = NXOpen.CAE.Post.AnimationType.Result
		animation1.AnimationStyle = NXOpen.CAE.Post.AnimationStyle.Linear
		animation1.NumberOfFrames = 8
		
		workSimPart = theSession.Parts.BaseWork
		#displaySimPart = theSession.Parts.BaseDisplay
		simSimulation1 = workSimPart.FindObject("Simulation")
		simSolution1 = simSimulation1.FindObject("Solution[Solution 1]")
		simResultReference1 = simSolution1.Find("Structural")
		solutionResult1 = theSession.ResultManager.CreateReferenceResult(simResultReference1)
		loadcase1 = solutionResult1.Find("Loadcase[1]")
		iteration1 = loadcase1.Find("Iteration[1]")
		#resultType1 = iteration1.Find("ResultType[[Displacement][Nodal]]")
		#resultParameters1.SetGenericResultType(resultType1)
		
		animation1.AnimStartIteration = iteration1
		animation1.AnimEndIteration = iteration1
		animation1.IterationIncrement = 1
		animation1.FullCycle = False
		animation1.Delay = 200
		animation1.AnimationStreamline.ShowGuides = True
		animation1.AnimationStreamline.StreamSync = NXOpen.CAE.Post.StreamlineSynchronization.SeedPoint
		animation1.AnimationStreamline.ActiveRegionStartFactor = 0.0
		animation1.AnimationStreamline.ActiveRegionEndFactor = 1.0
		animation1.AnimationStreamline.NumberOfIncrements = 40
		animation1.AnimationStreamline.ContinuousPulse = True
		animation1.AnimationStreamline.NumberOfTimePeriods = 10
		animation1.AnimationStreamline.FramesPerPulse = 5.0
		animation1.AnimationStreamline.PulseDutycycle = 0.050000000000000003
		animation1.IterationType = NXOpen.CAE.Post.AnimationIterationTypes.NotSet
		animation1.IterValueType = NXOpen.CAE.BaseIteration.IterationValueType.ValueOf(8)
		theSession.Post.PostviewAnimationPlay(1, animation1)
		
		theSession.Post.PostviewAnimationControl(1, NXOpen.CAE.Post.AnimationControl.Stop, -1, True, -1)
		
		animation2 = NXOpen.CAE.Post.AnimationParameters()
		
		animation2.AnimationType = NXOpen.CAE.Post.AnimationType.Result
		animation2.AnimationStyle = NXOpen.CAE.Post.AnimationStyle.Linear
		animation2.NumberOfFrames = 8
		animation2.AnimStartIteration = iteration1
		animation2.AnimEndIteration = iteration1
		animation2.IterationIncrement = 1
		animation2.FullCycle = False
		animation2.Delay = 200
		animation2.AnimationStreamline.ShowGuides = True
		animation2.AnimationStreamline.StreamSync = NXOpen.CAE.Post.StreamlineSynchronization.SeedPoint
		animation2.AnimationStreamline.ActiveRegionStartFactor = 0.0
		animation2.AnimationStreamline.ActiveRegionEndFactor = 1.0
		animation2.AnimationStreamline.NumberOfIncrements = 40
		animation2.AnimationStreamline.ContinuousPulse = True
		animation2.AnimationStreamline.NumberOfTimePeriods = 10
		animation2.AnimationStreamline.FramesPerPulse = 5.0
		animation2.AnimationStreamline.PulseDutycycle = 0.050000000000000003
		animation2.IterationType = NXOpen.CAE.Post.AnimationIterationTypes.NotSet
		animation2.IterValueType = NXOpen.CAE.BaseIteration.IterationValueType.ValueOf(8)
		theSession.Post.PostviewAnimationPlay(1, animation2)
	
	"""
	Save animation GIF
	"""
	def saveAnimGIF(self, path, filename):
		theSession = NXOpen.Session.GetSession()
		NXOpen.UI.GetUI().NXMessageBox.Show("The path", NXOpen.NXMessageBox.DialogType.Information, (path + filename))
		theSession.Post.PostviewCaptureAnimatedGif(1, (path + filename), False, False)
