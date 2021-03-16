# Group members: Håkon Bakke & Valeria Usenco
# KBE Project Course - Assignment 2 - Weldability check
# Introduction
The task chosen is to design a system to be able to check the weldability of a structure, based on the structure geometry and welding robot dimensions. The system should allow a user to specify the geometry of their design, so that a weldability check can be performed. In this case, the user can upload an image of their design. In this assignment, improvements from the last assignment are highlighted at the end of each section.

# Design Overview
## User Interface
The image below shows an overview of the user interface for the weldability check tool. The customer uploads a 2D image in addition to parameters for overall size and robot space. This gets analysed and after the customer clicks "submit". The user will then be sent to the results page where they have the option to receive the results by email as well as instantly getting them in the browser.

The web-page is divided into sections so as to not overwhelm the user with too many options. The buttons have defined with the principle of "affordance" in mind. Specifically, they have a shadow underneath, so that they represent a physical button more closely and invite the user to click them. The colours in the web-page are light and simple, so that the web-page is not overwhelming to look at. Another principle that has been used in this interface design is "mapping". The submit button is placed at the bottom right-hand corner, which is a natural placement for a button which triggers a process to go to the next stage. The buttons also change colour and the cursor changes to a hand when the user hovers over them.

![](Figures/A2/User_interface_assignment_2.png)

The feedback is given in the form of a picture, using red and green colours. An advantage of using these colours is that they are are naturally associated with whether something is or is not possible. However, they can also be challenging for users that are colourblind. Therefore, two different shading patterns have been added to the colour regions, so that colourblind users would be able differentiate the regions more easily. Again, the results web-page is divided into sections, to guide the user and not overwhelm them. The button also has the action described on it. 

:star: To highlight some improvements compared to the last assignment, the user interface is more interactive with direct visual feedback to the user in the form of changing colours or changing the cursor. The new UI is still plain, but uses some colours to make the buttons stand out more. In addition to this, common icons are used so reassure the user of the meaning of the buttons such as upload and download.

## Architecture
A high-level suggestion for the architecture is shown in the figure below. The customer interacts with the home page, which is hosted by customer_architect.py on the weldability check server. The architect is the main code block which unites the code utilities. The weldability check server also interacts with the knowledge-base server to store information. 

![](Figures/A2/Block_architecture.png)

A more in-depth description of the architecture is shown in the class diagram below. The process starts with an input image, which is preprocessed before the walls are extracted from it. Wall objects store the length and position of each wall found in the picture. They are turned into Block objects and combined to create an NX_model, and used to create a plot signifying which areas are weldable or not.  

![](Figures/A2/class_diagram.png)

# Implementation
The figures below shows the actual design of the web-interface for the task.  

![](Figures/A2/UI-home.PNG)

![](Figures/A2/UI-results.PNG)





