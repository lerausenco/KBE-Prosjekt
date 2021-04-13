from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from utils.parsers import  *
from os import curdir, sep
from utils.myHandler import myHandler
from utils.find_correct_material import find_stiff_and_cheap, find_stiffest_and_lightest, find_strongest_and_lightest
from utils.extract_data_from_website import find_dollar_cost_per_kg, web_table_to_dictionary
import json

data = web_table_to_dictionary()
materials=[]

materials.append( {'name':'AISI_Steel_4340'       , 'rho':7.8, 'E1': 210, 'E2':220,'XT':600, 'priceUSD_per_kg':find_dollar_cost_per_kg(data,"Steel"), 'fracture_thoughness':55, 'yield_strength':300} )
materials.append( {'name':'Aluminium'             , 'rho':2.7, 'E1':  70, 'E2': 70,'XT':310, 'priceUSD_per_kg':find_dollar_cost_per_kg(data,"Aluminium"), 'fracture_thoughness':33, 'yield_strength':270} )
materials.append( {'name':'Copper alloy'          , 'rho':8.3, 'E1':  120, 'E2': 120,'XT':345, 'priceUSD_per_kg':find_dollar_cost_per_kg(data,"Copper"), 'fracture_thoughness':1, 'yield_strength':310} )
materials.append( {'name':'Titan '                , 'rho':4.5, 'E1':  110, 'E2': 110,'XT':1000, 'priceUSD_per_kg':115, 'fracture_thoughness':71, 'yield_strength':760} )
materials.append( {'name':'Bamboo '               , 'rho':1.16, 'E1':  25, 'E2': 110,'XT':150, 'priceUSD_per_kg':0.94,} ) # https://dir.indiamart.com/impcat/bamboo-scaffolding.html?biz=10, https://www.bambooimport.com/en/what-are-the-mechanical-properties-of-bamboo


class NASTRAN_handler(myHandler):
    def do_GET(self):
        """
            Respond to a GET request.
            Images require their own file Content-type to be sent,
            so the send_image function is used to be able to display them.
        """
        #query fuseki and get params
        json_data = query_fuseki()
        node_list = parse_json(json_data)

        # find desired material
        if node_list[-1]["material_pref"] == "stiff_light":
            material = find_stiffest_and_lightest(materials[0],materials[1])['name']
        elif node_list[-1]["material_pref"] == "strong_light":
            material = find_strongest_and_lightest(materials[0],materials[1])['name']
        elif node_list[-1]["material_pref"] == "stiff_cheap":
            material = find_stiff_and_cheap(materials[0],materials[1])['name']


        #update with material choice
        node_list[-1]["material_pref"] = material

        #write list to txt file so openNX script can read it
        for node in node_list:
            #clear file
            f = open("params.txt", "w").close()
            f = open("params.txt", "a")
            f.write(str(node)+"\n")

        
        #quick feedback so we know server is running
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("NASTRAN ready", "utf-8"))
        return
     
    
