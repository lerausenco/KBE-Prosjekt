
# Group members: Håkon Bakke & Valeria Usenco
# KBE Project Course - Assignment 3 - Node validator and recommender
# Introduction
The task chosen is to create a system that can recommend what material to use in scaffolding nodes based on geometric parameters and load as input parameters. The system performs a finite element analysis (FEA) on the part by applying the forces specified by the user and gives feedback in the form of a gif of the FEA, and material recommendations. 

# Design Overview
## User Interface
The image below shows an overview of the user interface for the node calculation tool where the user can enter parameters and receive feedback.

![](Figures/A3/UI.png)

The feedback is given in the form of bullet points in addition to an image of an FEA simulation.

## Architecture
The architecture is shown in blocks in the figure below, with a short description of what the modules in each block do, and which modules interact with each other. 

![](Figures/A3/architecture3.png)

Below is a UML sequence diagram which shows the a typical usage scenario for the system from both the customer and manufacturer side. The user can enter loads and dimensions and receives results through a web-browser, while the manufacturer only needs to start the server and play the NX journal.

![](Figures/A3/UML3.png)

A more detailed description of the architecture is shown in the class diagram below. The diagram shows that myHandler is a class based on the BaseHTTPRequestHandler, which is a parent class for customer_handler and NASTRAN_handler. These both utilise functions in parsers.py which contains parser-functions and query-functions. NASTRAN_handler also calls the functions to choose the correct material through the use of external modules. The Duralok class is made up of Cylinders and Cones, which are NXOpen Features. The geometry of the duralok joint is defined there, along with the functions needed to perform an automatic FEA.

![](Figures/A3/class-diagram3.png)

:star: One improvement from the previous assignments is that the architecture uses class inheritance, which allows two different handlers to be defined based on myHandler. This allows for common functions to be reused without copying code. The functions in the handler have been reused from assignment 2. It is also worth mentioning that the send_image() function from assignment 2 was easy to extend to be able to handle .gifs in addition to .png and .jpg files. Another new feature is that one of the modules, more specifically traidingeconomics.com, retrieves live data and feeds it into the knowledge-based system. 

# Implementation

## UI
Below are screenshots of the actual UIs. The input UI is very similar to the UI sketch, however the results UI is different as it was deemed unnecessary to suggest two materials.

![](Figures/A3/UI-input.PNG)

![](Figures/A3/UI-res.PNG)

## Code Modules

* duralok.py - This contains the class for the duralok node. The class has all the functions needed for the node to be built up parametrically from cones and cylinders, perform FEA simulations and make a gif.
* myHandler.py - Custom handler with helper functions, derived from BaseHTTPRequestHandler.
* customer_handler.py - Child of myHandler with redefined do_POST() and do_GET() methods to host customer server. Uploads the loads and dimensions defined by the customer to the Fuseki database.
* NASTRAN_handler.py - Child of myHandler with redefined do_POST() and do_GET() methods to host NASTRAN server. Queries the fuseki database and finds the most recent addition. Writes the parameters of the most recent addition to params.txt, so that the play_NX scripts can read them.
* parsers.py - helper functions to parse json data and generate query text.
* extract_data_from_website.py - scripts to extract live material information from a website.
* find_correct_material.py - scripts to find the correct material based on specified criteria.
* play_NX_min.py - this is the journal to be played in NX to generate analysis with minimum loads. It creates a parametric model of the node using the parameters specified by the user. Then, using the methods in the Duralok class it goes through all the steps necessary to create a gif of the FEA simulation for the user. 
* play_NX_max.py - same as above but for maximum loads.
* run_customer_server.py - script to run the customer server in the terminal.
* run_NASTRAN_server.py - script to run the NASTRAN server in the terminal.

:star: As in assignments 1 and 2, the use of dictionaries makes it easy to add new attributes to the ontology. To add a new attribute, all that needs to be done with the code is the 'values' dictionary in parsers.py needs to be updated with the new attribute as a key. The update/query functions then take care of the rest. However, the .owl file must also be updated. 
An improvement concerning the database is the new naming system for node entries. The name of the node in this assignment is the data and time which the user submitted the order in the following format <YYMMDDHHMMSS>. This allows for NASTRAN_handler to easily sort the entries by time, and perform simulations on the newest entry, contrary to the first assignment, where the NX-generating module checked if a part with the same name existed, before generating it. Finally, it is also worth mentioning that the play_NX scripts give maximum automation - the script covers everything from opening creating a new part file, generating the part and saving it, meshing the part, running the analysis, creating and saving the gif and closing the part file. The operator only needs to open NX and press play.

# Examples from run-through
Different material preferences and load dimensions are demonstrated in each example.
## Example 1
### Inputs from user and generated part, the material will be Aluminium:

![](Figures/A3/node_example1.png)

### Results:

<img src="Figures/A3/node1_max.gif" width="470" height="400"> <img src="Figures/A3/node1_min.gif" width="470" height="400">

## Example 2

### Inputs from user and generated part, this time the material will be Steel:

![](Figures/A3/node_example2.png)

### Results:

<img src="Figures/A3/node2_max.gif" width="470" height="400"> <img src="Figures/A3/node2_min.gif" width="470" height="400">

## Example 3

### Inputs from user and generated part.

![](Figures/A3/node_example3.png)

### Results:
The deformation legend shows that the deformation is much larger.

<img src="Figures/A3/node3_max.gif" width="470" height="400"> <img src="Figures/A3/node3_min.gif" width="470" height="400">


# Video
Below is a video of the run-through, sped up 2x.
![](Figures/A3/fast-video.gif)

# Extendability and Improvements
Regarding extendability, it is easy to implement new materials, should the manufacturer be interested in working with other standard metals. Furthermore, the live cost for all the most common metals is already stored in a dictionary. Extending the ontology to take into account more user inputs is also easy to do, as the database queries and updates can be easily adapted to accomodate extra parameters. The use of website-data demonstrates the potential for extending the system as data from other sources can be implemented in the system in the same manner. Another factor which improves the extendibility is the parametric design of the node. The model of the node is generated based on the scaffolding pipe diameter and thickness. Although this resulted in challenges when developing the automatic analysis code, it provides flexibility for the user who can perform an automatic FEA analysis for pipes of different sizes simply by changing the diameter parameter. 

That being said, the current implementation would require a more robust process for the selection of faces for where the forces are applied. Currently, the scaffolding pipe diameter can only be varied over a relatively small range (ca. ±10cm), before openNX struggles to find the face specified and gives an error. This is not ideal, however this range may be sufficient for this application which uses standardised components.

Another drawback is that the current implementation requires an operator to run the FEA script in NX in order to perform the analysis. Ideally, this feature would be changed such that a Python script opens NX automatically, which would ensure a seamless connection from user to feedback. Another feature that could be implemented in the future is topology optimization. The user can then input the design space and loads in the UI and the system performs a topology optimisation and FEA on the geometry.

# Conclusion
A KBE system for proposing node material and running a FEA simulation was successfully implemented. The system connects different modules with information and knowledge flowing between them by updating and quering a Fuseki server. The system demonstrates on a low level, how intedisciplinary engineering modules can interact with each other. More specifically, it includes a materials module which interacts with a finite element analysis module. Feedback is given to the user in the form of a suggested best-fit material and FEA deformation results, based on input as load and material characteristics from the user. Finally, many utility functions were reused from previous assignments.
Although this is by no means an ideal systems, it serves as a proof of concept for the potential modules that can be tied together to make a KBE system


