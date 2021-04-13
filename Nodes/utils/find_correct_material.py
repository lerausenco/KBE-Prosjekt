from extract_data_from_website import find_dollar_cost_per_kg, web_table_to_dictionary

data = web_table_to_dictionary()

materials=[]
materials.append( {'name':'Steel'                 , 'rho':7.8, 'E1': 210, 'E2':220,'XT':600, 'priceUSD_per_kg':find_dollar_cost_per_kg(data,"Steel"), 'fracture_thoughness':55, 'yield_strength':300} )
materials.append( {'name':'Aluminium'             , 'rho':2.7, 'E1':  70, 'E2': 70,'XT':310, 'priceUSD_per_kg':find_dollar_cost_per_kg(data,"Aluminium"), 'fracture_thoughness':33, 'yield_strength':270} )
materials.append( {'name':'Copper alloy'          , 'rho':8.3, 'E1':  120, 'E2': 120,'XT':345, 'priceUSD_per_kg':find_dollar_cost_per_kg(data,"Copper"), 'fracture_thoughness':1, 'yield_strength':310} )
materials.append( {'name':'Titan '                , 'rho':4.5, 'E1':  110, 'E2': 110,'XT':1000, 'priceUSD_per_kg':115, 'fracture_thoughness':71, 'yield_strength':760} )
materials.append( {'name':'Bamboo '               , 'rho':1.16, 'E1':  25, 'E2': 110,'XT':150, 'priceUSD_per_kg':0.94,} ) # https://dir.indiamart.com/impcat/bamboo-scaffolding.html?biz=10, https://www.bambooimport.com/en/what-are-the-mechanical-properties-of-bamboo




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


print(find_stiffest_and_lightest(materials[0],materials[1]))


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

print(find_strongest_and_lightest(materials[0],materials[1]))

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


print(find_stiff_and_cheap(materials[0],materials[1]))

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

