import os
import sys

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import json

HOST_NAME = 'localhost'
FACT_PORT_NUMBER = 2410


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
        chair_data = parseJson(jsonData)
        #makeDFA(table_data)
        #html_chair_data = OrderOverView(chair_data)
        html_code = getHTMLstring("factory_overview.html")
        #html_code = html_code.replace("<p> No orders yet </p>", html_chair_data)
        s.wfile.write(bytes(html_code, "utf-8"))

        str_path = s.path

def getOrder():
    chair_params = { 'name':0, 's_width': 0, 's_depth': 0, 'a_th': 0, 'with_arm': 0, 'with_back': 0,
             'back_height': 0, 'with_top': 0, 'top_th': 0, 'with_mid': 0, 'mid_th': 0,
             'with_bot': 0, 'bot_th': 0 , 'leg_height': 0, 'leg_th': 0, 'with_taper': 0,
             'spindles': 0 }
    chair_param = ['name', 's_width', 's_depth', 'a_th', 'with_arm', 'with_back' \
                'back_height', 'with_top', 'top_th', 'with_mid', 'mid_th'\
                'with_bot', 'bot_th', 'leg_height', 'leg_th', 'with_taper'\
                'spindles']
    
    #chair_name = str(chair_param[0]) # + "x" +str(chair_param[1])
    where_str = '''?a_chair a kbe:chair. \n ''' 

    for key in chair_params:    
        where_str += ' ?a_chair kbe:'+key+'' ' ?'+key+ '. \n'  

    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY = '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT ?name ?s_width ?s_depth ?a_th ?with_arm ?with_back ?back_height ?with_top ?top_th ?with_mid ?mid_th ?with_bot ?bot_th ?leg_height ?leg_th ?with_taper ?spindles
            WHERE {
               '''+where_str+'''
            }
            '''
    #print("QUERY::", QUERY)
    PARAMS = {'query':QUERY}
    response = requests.post(URL,data=PARAMS)
    #print("Result of query:", response.text)
    json_data = response.json()
    #print("JSON", json_data)
    return json_data

def parseJson(json_data): #returns an array with parameters
    chair_parms = { 'name':0, 's_width': 0, 's_depth': 0, 'a_th': 0, 'with_arm': 0, 'with_back': 0,
             'back_height': 0, 'with_top': 0, 'top_th': 0, 'with_mid': 0, 'mid_th': 0,
             'with_bot': 0, 'bot_th': 0 , 'leg_height': 0, 'leg_th': 0, 'with_taper': 0,
             'spindles': 0 }
    #get sizes
    num_of_params = len(chair_parms)
    num_of_chairs = len(json_data['results']['bindings'])
    
    #print('printout from json: ', json_data['results']['bindings'][1]['name']['value'])
    for x in range(num_of_chairs):
        for key in chair_parms:
            chair_parms[key] = json_data['results']['bindings'][x][key]['value']
    print('dictionary with parms', chair_parms)
    chair_data = chair_parms
    return chair_data

def OrderOverView(chair_data):
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
        
    
    
    
