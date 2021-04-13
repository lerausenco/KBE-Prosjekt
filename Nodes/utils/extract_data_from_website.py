# importing the libraries
import pandas as pd
import requests
import numpy as np



def web_table_to_dictionary():
    """
           Reads website and find the relevant tables. 
           Extract the values and names and stores them in a dictionary named "data" and returns the data

        """

    url = "https://tradingeconomics.com/commodity/steel"
    url_currency = "https://tradingeconomics.com/currencies"
    metal_table = pd.read_html(url)[4]
    currency_table = pd.read_html(url_currency)[0]
    data = {}
    data[currency_table['Major'][5]] = currency_table['Price'][5] #extracts the exchange value for USDCNY
    for i in range(len(metal_table)): #itereate through all rows 
        data[metal_table['Industrial'][i]] = metal_table['Price'][i] # Extracts all the metal names and corresponding price
    return data

data = web_table_to_dictionary()

def find_dollar_cost_per_kg(data, metal):
    """
           Returns the live cost of a material in USD/kg

           args:
                data: dictionary with data crated from web_table_to_dictionary()
                metal: name of the material you want to know the cost price of
                Implemented: Aluminium, Steel, Copper

        """
    if metal == "Aluminium":
        key = "Aluminum USD/T" 
        return data[key]/1000  #Aluminium is stored in USD/ton so dividing by 1000 to get USD/kg
    elif metal == "Steel":
        key = "Steel CNY/T" #Steel is stored in CNY/ton so need to divide by 1000 and the exchange rate for USDCNY to get USD/kg
        return data[key]/(data['USDCNY']*1000) 
    elif metal == "Copper":
        key = "Copper USD/Lbs" #Copper is stored in USD/pound so dividing by 0.45  to get USD/kg
        return data[key]/0.45 
    else:
        print("Material not implemented")
        return False

"""
    Uncomment the lines below to test the find_dollar_cost_per_kg() function
"""
#lst_metals = ["Aluminium","Steel","Copper"]
#for key in lst_metals:
#    print("Price for: ", key, np.round(find_dollar_cost_per_kg(data,key),2), "USD/kg")



