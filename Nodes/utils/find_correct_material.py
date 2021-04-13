#from extract_data_from_website import find_dollar_cost_per_kg, web_table_to_dictionary





def find_stiffest_and_lightest(mat1,mat2):
    """
           Finds the stiffest and ligtest material

           args: 
                two materials as dictionary - mat1, mat2

           returns:
                Print message and returns the best fit material
        """
    if  (mat1['E1']/mat1['rho']) > (mat2['E1']/mat2['rho']):
        print(mat1['name'], "Is the stiffest and lightest")
        return mat1
    elif (mat1['E1']/mat1['rho'] < mat2['E1']/mat2['rho']):
        print(mat2['name'], "Is the stiffest and lightest")
        return mat2
    else:
        print("The materials have identical properties")
        return mat1, mat2





def find_strongest_and_lightest(mat1,mat2):
    """
           Finds the strongest and ligtest material

           args: 
                two materials as dictionary - mat1, mat2

           returns:
                Print message and returns the best fit material
        """
    if  (mat1['XT']/mat1['rho']) > (mat2['XT']/mat2['rho']):
        print(mat1['name'], "Is the strongest and lightest")
        return mat1
    elif (mat1['XT']/mat1['rho'] < mat2['XT']/mat2['rho']):
        print(mat2['name'], "Is the strongest and lightest")
        return mat2
    else:
        print("The materials have identical properties")
        return mat1, mat2

#print(find_strongest_and_lightest(materials[0],materials[1]))

def find_stiff_and_cheap(mat1,mat2):
    """
           Finds the stiffest and cheapest material

           args: 
                two materials as dictionary - mat1, mat2

           returns:
                Print message and returns the best fit material
        """

    if  (mat1['E1']/(mat1['rho'] * mat1['priceUSD_per_kg'])) > (mat2['E1']/(mat2['rho'] * mat2['priceUSD_per_kg'])):
        print(mat1['name'], "Is the stiffest and cheapest per mass")
        return mat1
    elif (mat1['E1']/(mat1['rho'] * mat1['priceUSD_per_kg'])) < (mat2['E1']/(mat2['rho'] * mat2['priceUSD_per_kg'])):
        print(mat2['name'], "Is the stiffest and cheapest per mass")
        return mat2
    else:
        print("The materials have identical properties")
        return mat1, mat2


#print(find_stiff_and_cheap(materials[0],materials[1]))

def compare_materials(names,xdata,ydata,xlabel,ylabel):
    """
           Makes a scatter plot of the different material values inputted.
           
           Inspired by https://folk.ntnu.no/nilspv/TMM4175/plot-gallery.html
           args: 
                names: name of material
                xdata: data along x-axis
                ydata: data along y-axis
                xlabel: label for x-axis
                ylabel: label for y-axis
    """
    import numpy as np
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(10,6))
    for k in range(len(names)):
        ax.text(xdata[k],ydata[k],names[k])
    ax.grid(True)
    ax.scatter(xdata, ydata, s=100, c='red', alpha= 0.6)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
