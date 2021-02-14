import os
import sys


from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import json

HOST_NAME = 'localhost'
CUST_PORT_NUMBER = 1024

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
        quantity = 0


        values = {} #stores the last chair generated
        
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
            
            print(values)
            addChair(values)

        if str_path.find("quantity")!=-1:
            quantity = str_path.split("?")[1]

            ###add order defined by dictionary "values", and quantity

        if str_path.find("customer_info")!=-1:
            data = str_path.split("?")
            params = data[1]
            pairs = params.split("&")

            name = pairs[0].split("=")[1]
            email = pairs[1].split("=")[1]

            ###add order defined by dictionary "values", and quantity

            print("values ",values)
           # addOrder(values, quantity, name, email)



def addChair(values):
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
    print("UPDATE QUERY:", UPDATE)
    PARAMS = {'update':UPDATE}
    response = requests.post(URL,data=PARAMS)
    print("Result:", response.text)


if __name__ == '__main__':
    customer_server = HTTPServer
    customer_httpd = customer_server((HOST_NAME, CUST_PORT_NUMBER), CustomerHandler)
    print(time.asctime(), "Customer Server - %s:%s" % (HOST_NAME, CUST_PORT_NUMBER))

    try:
        customer_httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    customer_httpd.server_close()
        