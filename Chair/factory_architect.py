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
       

        jsonData = getChairs()
        chair_list = parseJson(jsonData)
        json_order_data = getOrder()
        order_list = parseJsonOrder(json_order_data)
        #makeDFA(chair_list)
        html_chair_data = OrderOverView(chair_list, order_list)
        html_code = getHTMLstring("factory_overview.html")
        html_code = html_code.replace("<p> No orders yet </p>", html_chair_data)
        s.wfile.write(bytes(html_code, "utf-8"))

        str_path = s.path

def getChairs():
    chair_params = { 'name':0, 's_width': 0, 's_depth': 0, 'a_th': 0, 'with_arm': 0, 'with_back': 0,
             'back_height': 0, 'with_top': 0, 'top_th': 0, 'with_mid': 0, 'mid_th': 0,
             'with_bot': 0, 'bot_th': 0 , 'leg_height': 0, 'leg_th': 0, 'with_taper': 0,
             'spindles': 0  }    
    where_str = '''?a_chair a kbe:chair. \n ''' 
    select_str =""
    for key in chair_params:
        select_str += ' ?'+key
        where_str += ' ?a_chair kbe:'+key+'' ' ?'+key+ '. \n'  

    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY = '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT '''+select_str+ '''
            WHERE {
               '''+where_str+'''
            }
            '''
   # print("QUERY::", QUERY)
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
    chair_list = []
    #get sizes
    num_of_chairs = len(json_data['results']['bindings'])

    for x in range(num_of_chairs):
        for key in chair_parms:
            chair_parms[key] = json_data['results']['bindings'][x][key]['value']
        dic_copy = chair_parms.copy()
        chair_list.append(dic_copy)
    #print("Chair list",chair_list)    
    return chair_list

def getOrder():
    order_params = { 'name': 0, 'quantity': 0, 
                     'email': 0, 'status': 0  }
    
    where_str = '''?a_order a kbe:order. \n ''' 
    select_str =""
    for key in order_params:
        select_str += ' ?'+key
        where_str += ' ?a_order kbe:'+key+'' ' ?'+key+ '. \n'  

    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY = '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT '''+select_str+ '''
            WHERE {
               '''+where_str+'''
            }
            '''
   # print("QUERY::", QUERY)
    PARAMS = {'query':QUERY}
    response = requests.post(URL,data=PARAMS)
    #print("Result of query:", response.text)
    json_order_data = response.json()
    #print("JSON", json_data)
    return json_order_data
def parseJsonOrder(json_order_data): #returns an array with parameters
    order_params = { 'name': 0, 'quantity': 0, 
                     'email': 0, 'status': 0  }
    order_list = []
    #get sizes
    num_of_chairs = len(json_order_data['results']['bindings'])

    for x in range(num_of_chairs):
        for key in order_params:
            order_params[key] = json_order_data['results']['bindings'][x][key]['value']
        dic_copy = order_params.copy()
        order_list.append(dic_copy)
    print("order list",order_list)    
    return order_list

def OrderOverView(chair_list, order_list):
    #create html string to update factory overview table
    chair_parms = { 'name':0, 's_width': 0, 's_depth': 0, 'a_th': 0, 'with_arm': 0, 'with_back': 0,
             'back_height': 0, 'with_top': 0, 'top_th': 0, 'with_mid': 0, 'mid_th': 0,
             'with_bot': 0, 'bot_th': 0 , 'leg_height': 0, 'leg_th': 0, 'with_taper': 0,
             'spindles': 0 }
    #for key in chair_parms:
     #   print('first chair', chair_list[0][key])
    
    Msg = ''
    for x in range(len(chair_list)):
        Msg +='<tr>'
       # for key in chair_list[x]:
        Msg += '<td>'+chair_list[x]['name']+'</td>''<td>'+order_list[x]['name']+'</td>''<td>'+order_list[x]['email']+'</td>''<td>'+order_list[x]['quantity']+'</td>''<td>'+order_list[x]['status']+'</td>'
        Msg += '</tr>'
    
    return Msg

def makeDFA(chair_list):
    
    template_path = "DFA\\Templates\\Chair_base.dfa"
    f = open(template_path, "r")
    dfa_txt = f.read()

    for i in range(len(chair_list)):

        if (not os.path.isfile("DFA\\Orders\\"+chair_list[i]['name']+".dfa")): #check if file already exists
            
            #create new dfa file with chair name
            order_dfa = open("DFA\\Orders\\"+chair_list[i]['name']+".dfa", "w")


            #write number parameters into dfa file

            for key in chair_list[i]:
                #print("NAMES: ", chair_list[i]['name'])
                dfa_txt = dfa_txt.replace("<"+key+">", chair_list[i][key])
            
            order_dfa.write(dfa_txt)

            #write extra features
            #print(chair_list[i])

            if (chair_list[i]['with_arm']!="0"):
                feature_file = open("DFA\\Templates\\arm_support.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)

            if (chair_list[i]['with_back']!="0"):
                feature_file = open("DFA\\Templates\\Back.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)

            if (chair_list[i]['with_top']!="0"):
                feature_file = open("DFA\\Templates\\rail-top.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)
            
            if (chair_list[i]['with_mid']!="0"):
                feature_file = open("DFA\\Templates\\rail-mid.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)

            if (chair_list[i]['with_bot']!="0"):
                feature_file = open("DFA\\Templates\\rail-bot.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)

            if (chair_list[i]['with_taper']!="0"):
                feature_file = open("DFA\\Templates\\taper.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)

            if (int(chair_list[i]['spindles']) > 0):
                feature_file = open("DFA\\Templates\\spindles.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)
            
            if (int(chair_list[i]['spindles']) > 2):
                feature_file = open("DFA\\Templates\\spindles3.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)
            
            if (int(chair_list[i]['spindles']) > 3):
                feature_file = open("DFA\\Templates\\spindles4.txt", "r")
                feature_txt = feature_file.read()
                order_dfa.write(feature_txt)


            order_dfa.close()

if __name__ == '__main__':
    factory_server = HTTPServer
    factory_httpd = factory_server((HOST_NAME, FACT_PORT_NUMBER),FactoryHandler)
    print(time.asctime(), "Factory Server - %s:%s" % (HOST_NAME, FACT_PORT_NUMBER))

    try:
        factory_httpd.serve_forever()

    except KeyboardInterrupt:
        pass
    
    factory_httpd.server_close()