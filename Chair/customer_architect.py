import os
import sys


from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import json

HOST_NAME = 'localhost'
CUST_PORT_NUMBER = 1024

values = {} #stores the last chair generated
chair_name = ""
quantity = 0

def getHTMLstring(file_name):
    f = open(os.path.join(sys.path[0], file_name), "r")
    return f.read()

class CustomerHandler(BaseHTTPRequestHandler):
    
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        html_code = getHTMLstring("CustomerUI.html")
        s.wfile.write(bytes(html_code, "utf-8"))

        str_path = s.path

        #extract chair dimensions on "Preview button press"
        if str_path.find("product_info")!=-1:
            str_path = str_path.replace("+", "_")
            data = str_path.split("?")
            params = data[1]
            pairs = params.split("&") #key value pairs

            for i in range(len(pairs)):
                param_value = pairs[i].split("=")[1]
                if param_value == '':
                    values[pairs[i].split("=")[0]] = 0
                else:
                    values[pairs[i].split("=")[0]] = param_value

        #add quantity
        if str_path.find("order_info")!=-1:
            quantity_key_pair = str_path.split("?")[1]
            quantity = quantity_key_pair.split("=")[1]
            values['quantity'] = quantity
        
        #get customer info
        if str_path.find("customer_info")!=-1:
            str_path = str_path.replace("+", "_")
            data = str_path.split("?")
            params = data[1]
            pairs = params.split("&")

            name = pairs[0].split("=")[1]
            email = pairs[1].split("=")[1]
            email = email.replace("%40", "@")

        #send an order into the database
            quantity = values['quantity']            
            chair_name = addChair(values) #add chair to factory database
            addOrder(chair_name, quantity, name, email) #add order to factory database

         #display estimated time of arrival   
            html_code = writeTimeEstimate()
            s.wfile.write(bytes(html_code, "utf-8"))

def getQuantity():
    #get the total amount of chairs waiting to be produced



    ##status???
    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY =    '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT ?quantity
            WHERE {
                ?an_order a kbe:order.
                ?an_order kbe:quantity ?quantity.
                }
            '''
    PARAMS = {'query':QUERY}
    response = requests.post(URL,data=PARAMS)
    json_data = response.json()

    num_of_orders = len(json_data['results']['bindings'])
    quantity = 0
    for i in range(num_of_orders):
        quantity += int(json_data['results']['bindings'][i]["quantity"]["value"])
    return quantity

def estimateTime():
    #calculate an estimate for how long the customer has to wait (arbitray formula)
    quantity = getQuantity()
    days = quantity % 10 + 1 #can make 10 chairs a day + extra day for packing
    return days

def writeTimeEstimate():
    #update the html file with the number of days
    days = estimateTime()
    html_code = getHTMLstring("order_complete.html")
    html_code = html_code.replace("xxx", str(days))
    return html_code

def addChair(values):
    #add chair design to database
    values.pop("quantity") #do not want to add quantity to chair class
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
    
    PARAMS = {'update':UPDATE}
    print("Update query:", UPDATE)
    response = requests.post(URL,data=PARAMS)
    return chair_name

def addOrder(chair_name, quantity, name, email):
    #add order to database
    orderID = name + chair_name

    URL = "http://127.0.0.1:3030/kbe/update"
    UPDATE = '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT
            {
             kbe:order_''' +orderID+ ''' a kbe:order. 
             kbe:order_''' +orderID+ ''' kbe:name "'''+name+ '''".
             kbe:order_''' +orderID+ ''' kbe:quantity "'''+str(quantity)+'''"^^xsd:float.
             kbe:order_''' +orderID+ ''' kbe:email "'''+email+'''".
             kbe:order_''' +orderID+ ''' kbe:status "0"^^xsd:float.            
            }
            WHERE
            { 
            }  
    '''
    PARAMS = {'update':UPDATE}
    response = requests.post(URL,data=PARAMS)
   

if __name__ == '__main__':
    customer_server = HTTPServer
    customer_httpd = customer_server((HOST_NAME, CUST_PORT_NUMBER), CustomerHandler)
    print(time.asctime(), "Customer Server - %s:%s" % (HOST_NAME, CUST_PORT_NUMBER))

    try:
        customer_httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    customer_httpd.server_close()
        