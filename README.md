# KBE Project Course - Assignment 1 - Chair
## Introduction

This page describes the process of creating a KBE system for customisable chairs. The system should allow customers to design their own chair through a web-based user interface (UI). 

## Development
### Customer Interface
The customer interface has been designed in draw.io, to serve as a template for the HTML-code. It is important for the customer UI to be user-friendly and easy to use. With this in mind, the parameters for each part of the chair have been split up into sections, so that the user does not get overwhelmed with a long list of parameters. If the user is unsure about what each parameter refers to, they can click the help button which reveals an annotated image of a chair to inform the user about which parameter they can change. Below is a sketch of how the user interface could be designed.

![](Figures/CustomerUI.png)

After providing the parameters and pressing the Preview button, a model should be generated and shown in the window on the right. The user can then either choose to add a number of chairs to their order, or generate a new chair by changing the parameters and pressing the Preview button again. The customer can preview and edit it in the menu in the top right corner. When the customer is ready to submit their order, they must provide their contact details, and press submit order. They are then redirected to a page where they get to know the estimated arrival time of their order. The steps of a customer order are shown in the flowchart below.

![](Figures/Process.png)


###Factory Interface