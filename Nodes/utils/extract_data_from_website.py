# importing the libraries
import pandas as pd
import requests
import numpy as np



def web_table_to_dictionary():
    url = "https://tradingeconomics.com/commodity/steel"
    url_currency = "https://tradingeconomics.com/currencies"
    metal_table = pd.read_html(url)[4]
    currency_table = pd.read_html(url_currency)[0]
    data = {}
    data[currency_table['Major'][5]] = currency_table['Price'][5]
    for i in range(len(metal_table)):
        data[metal_table['Industrial'][i]] = metal_table['Price'][i]
    return data
#print(metal_table['Industrial'][3], metal_table['Price'][3])
#print(currency_table)
#print(currency_table['Major'][5], currency_table['Price'][5])

data = web_table_to_dictionary()

#print(web_table_to_dictionary())

def find_dollar_cost_per_kg(data, metal):
    if metal == "Aluminium":
        key = "Aluminum USD/T"
        return data[key]/1000
    elif metal == "Steel":
        key = "Steel CNY/T"
        return data[key]/(data['USDCNY']*1000)
    elif metal == "Copper":
        key = "Copper USD/Lbs"
        return data[key]/0.45
    else:
        return False
lst_metals = ["Aluminium","Steel","Copper"]
for key in lst_metals:
    print("Price for: ", key, np.round(find_dollar_cost_per_kg(data,key),2), "USD/kg")
#print (table['Industrial'])
#print (table['Industrial']['Steel CNY/T'])


