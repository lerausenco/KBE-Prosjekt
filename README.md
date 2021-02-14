# KBE Project Course - Assignment 1 - Chair
# Introduction

This page describes the process of creating a KBE system for customisable chairs. The system should allow customers to design their own chair through a web-based user interface (UI). 

# Development Overview
## Customer Interface
The customer interface has been designed in draw.io, to serve as a template for the HTML-code. It is important for the customer UI to be user-friendly and easy to use. With this in mind, the parameters for each part of the chair have been split up into sections, so that the user does not get overwhelmed with a long list of parameters. If the user is unsure about what each parameter refers to, they can click the help button which reveals an annotated image of a chair to inform the user about which parameter they can change. Below is a sketch of how the user interface could be designed.

![](Figures/CustomerUI.png)

After providing the parameters and pressing the Preview button, a model should be generated and shown in the window on the right. The user can then either choose to add a number of chairs to their order, or generate a new chair by changing the parameters and pressing the Preview button again. The customer can preview and edit it in the menu in the top right corner. When the customer is ready to submit their order, they must provide their contact details, and press submit order. They are then redirected to a page where they get to know the estimated arrival time of their order. The steps of a customer order are shown in the flowchart below.

![](Figures/Process.png)


## Factory Interface
The factory could also have a simple interface showing the order overview. A suggestion is shown in the figure below. The production manager could for example log into the factory web interface and view the orders that have come in from the customers. The suggestion below also shows a menu to be able to edit the order status or view the design.

![](Figures/factoryUI.png)

## Architecture

A KBE architecture suggestion is shown in the figure below. The customer interacts with the customer UI, where they can design their own chair by writing in dimensions, and selecting what sort of features they would like. Upon pressing preview, an image of their design would come up in the picture box. After submitting an order, the customer gets a "Thank you" message with an estimated time of arrival (ETA) for their order. The ETA is calculated in the customer_architect.py file by checking how many active orders the manufacturer has.

![](Figures/Architecture.png)

The database ontology is defined by Chairs.owl, which holds definitions for two classes, Order and Chair. Next, the factory_architect.py script serves for several purposes. The architect creates .dfa files from incoming orders by using the Chair_base.dfa file along with the 'features' files containing features that can be selected with the checkboxes. The features are stored as .txt files because they are only used to fill out the base .dfa file. The resulting output is the Chair_order.dfa file which can be viewed in Siemens NX. The factory_architect.py script also displays an order overview, and serves as a user interface for the production manager, who can use it to mark orders as complete.

# Implementation
## Customer User Interface
The image below shows the actual implementation of the customer UI for this task. The image of the chair is static, but represents a live model of the customer's design after pressing "Preview".
![](Figures/UI-screenshot.png)

## Factory User Interface


### customer_architect.py
The customer architect responds to a GET-request triggered by pressing one of the buttons on the customer UI. 

Pressing the preview button parses the URL and extracts the parameters using string manipulation functions. The parameters are stored in a dictionary called 'values'.

Pressing the Add to Order button records the value written in the Quantity text box.

Pressing the Submit button adds the chair design to the database. It also adds an order with the name of the chair design, the quantity, customer name and email. Finally, a "thank you" message is displayed, as well as an estimate of the ETA for the customer's order.

The code to create the update string used to add a chair design to the database uses a for-loop to save time.

```python
chair_name = str(values['s_width']) + "x" +str(values['s_depth'])
    insert_str = '''kbe:chair_''' + chair_name +  ''' a kbe:chair.
                    kbe:chair_''' + chair_name + ''' kbe:name "'''+chair_name+ '''".\n''' 

    for key in values:
        insert_str += 'kbe:chair_'+chair_name+ ' kbe:'+ key +' "' + str(values[key])+ '"^^xsd:float. \n'  

    URL = "http://127.0.0.1:3030/kbe/update"
    UPDATE = '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT
            {
             '''+insert_str+'''             
            }
            WHERE
            { 
            } 
            '''
```
