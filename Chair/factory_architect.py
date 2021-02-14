import os
import sys

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import json

HOST_NAME = 'localhost'
FACT_PORT_NUMBER = 2410

chair_params = ['s_width', 's_depth', 'a_th', 'with_arm', 'with_back' \
                'back_height', 'with_top', 'top_th', 'with_mid', 'mid_th'\
                'with_bot', 'bot_th', 'leg_height', 'leg_th', 'with_taper'\
                'spindles']

def getHTMLstring(file_name):
    f = open(os.path.join(sys.path[0], file_name), "r")
    return f.read()

class FactoryHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        jsonData = getOrder()
        table_data = parseJson(jsonData)
        makeDFA(table_data)
        html_table_data = OrderOverView(table_data)
        html_code = getHTMLstring("factory_overview.html")
        html_code = html_code.replace("<p> No orders yet </p>", html_table_data)
        s.wfile.write(bytes(html_code, "utf-8"))
        

        #str_path = s.path

def getOrder():
    

    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY = '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT ?table_name ?tl_leg_height ?tl_leg_thickness ?tl_leg_width ?tt_depth ?tt_thickness ?tt_width
            WHERE {
                ?table_name a kbe:Table.
                ?table_name kbe:Leg_height ?tl_leg_height.
                ?table_name kbe:Leg_thickness ?tl_leg_thickness.
                ?table_name kbe:Leg_width ?tl_leg_width.
                ?table_name kbe:TableTop_depth ?tt_depth.
                ?table_name kbe:TableTop_thickness ?tt_thickness.
                ?table_name kbe:TableTop_width ?tt_width.
            }
            '''
    PARAMS = {'query':QUERY}
    response = requests.post(URL,data=PARAMS)
    print("Result of query:", response.text)
    json_data = response.json()
    #print("JSON", json_data)
    return json_data

def parseJson(json_data): #returns an array with parameters
   
    param_names = ['table_name', 'tl_leg_height', 'tl_leg_thickness', 'tl_leg_width', 'tt_depth', 'tt_thickness', 'tt_width']
    
    #get sizes
    num_of_params = len(param_names)
    num_of_tables = len(json_data['results']['bindings'])

    #make empty array to store table data
    table_data = [[0 for x in range(num_of_params)] for y in range(num_of_tables)]
    
    #populate array
    for j in range(num_of_tables):
        table_data[j][0] = json_data['results']['bindings'][j][param_names[0]]['value'].split("#")[1] #get name of table
        for i in range(1, len(param_names)):
            table_data[j][i] = json_data['results']['bindings'][j][param_names[i]]['value']
    
    print(table_data)    
    return table_data

def OrderOverView(table_data):
    #create html string to update factory overview table
    Msg = ''
    for i in range(len(table_data)):
        Msg +='<tr>'
        for j in range(len(table_data[i])):
            Msg += '<td>'+table_data[i][j]+'</td>'
        Msg += '</tr>'
    
    return Msg

def makeDFA(table_data):
    PARAM_LIST = ['<TABLE_NAME>','<TL_HEIGHT>','<TL_THICKNESS>','<TL_WIDTH>', '<TT_DEPTH>','<TT_THICKNESS>','<TT_WIDTH>']

    template_path = "Templates\\Table.dfa"
    f = open(template_path, "r")
    dfa_txt = f.read()

    for i in range(len(table_data)): 
        if (not os.path.isfile("Orders\\"+table_data[i][0]+".dfa")): #check if file already exists
            #create new dfa file with table name
            order_data = table_data[i]
            order_dfa = open("Orders\\"+order_data[0]+".dfa", "w")
            #write parameters into dfa file
            for i in range(len(PARAM_LIST)):
                dfa_txt = dfa_txt.replace(PARAM_LIST[i], order_data[i])

            order_dfa.write(dfa_txt)
            order_dfa.close()

    return

if __name__ == '__main__':
    factory_server = HTTPServer
    factory_httpd = factory_server((HOST_NAME, FACT_PORT_NUMBER),FactoryHandler)
    print(time.asctime(), "Factory Server - %s:%s" % (HOST_NAME, FACT_PORT_NUMBER))

    try:
        factory_httpd.serve_forever()

    except KeyboardInterrupt:
        pass
    
    factory_httpd.server_close()
        
    
    
    
