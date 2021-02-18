import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests

HOST_NAME = "localhost"
CUST_PORT_NUMBER = 1024

values = {}  # stores the last chair generated
chair_name = ""
quantity = 0


def get_HTML_string(file_name):
    f = open(os.path.join(sys.path[0], file_name), "r")
    return f.read()


class CustomerHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html_code = get_HTML_string("CustomerUI.html")
        self.wfile.write(bytes(html_code, "utf-8"))

        str_path = self.path

        # extract chair dimensions on "Preview button press"
        if str_path.find("product_info") != -1:
            str_path = str_path.replace("+", "_")
            data = str_path.split("?")
            params = data[1]
            pairs = params.split("&")  # key value pairs

            for i in range(len(pairs)):
                param_value = pairs[i].split("=")[1]
                if param_value == "":
                    values[pairs[i].split("=")[0]] = 0
                else:
                    values[pairs[i].split("=")[0]] = param_value

        # add quantity
        if str_path.find("order_info") != -1:
            quantity_key_pair = str_path.split("?")[1]
            quantity = quantity_key_pair.split("=")[1]
            values["quantity"] = quantity

        # get customer info
        if str_path.find("customer_info") != -1:
            str_path = str_path.replace("+", "_")
            data = str_path.split("?")
            params = data[1]
            pairs = params.split("&")

            name = pairs[0].split("=")[1]
            email = pairs[1].split("=")[1]
            email = email.replace("%40", "@")

            # get quantity
            quantity = values["quantity"]

            # get max and min values
            json_data_max_lim = get_limit("MAX")
            json_data_min_lim = get_limit("MIN")
            max_list = parse_json(json_data_max_lim)
            min_list = parse_json(json_data_min_lim)

            # check if inputs are ok
            ok = feedback_to_customer(values, min_list, max_list)

            # write a message based on if order is ok
            html_code = write_message(ok)
            self.wfile.write(bytes(html_code, "utf-8"))

            # send an order into the database if inputs are ok
            if ok:
                # add chair design to factory database
                chair_name = add_chair(values)
                add_order(
                    chair_name, quantity, name, email
                )  # add order to factory database


def get_quantity():
    # get the total amount of chairs waiting to be produced
    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY = """
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT ?quantity ?status
            WHERE {
                ?an_order a kbe:order.
                ?an_order kbe:quantity ?quantity.
                ?an_order kbe:status ?status.
                }
            """
    PARAMS = {"query": QUERY}
    response = requests.post(URL, data=PARAMS)
    json_data = response.json()

    num_of_orders = len(json_data["results"]["bindings"])
    quantity = 0
    for i in range(num_of_orders):
        status = json_data["results"]["bindings"][i]["status"]["value"]
        if status == "0":  # only count chairs still waiting to be produced
            quantity += int(json_data["results"]["bindings"][i]["quantity"]["value"])
    return quantity


def estimate_time():
    # calculate an estimate for how long the customer has to wait
    quantity = get_quantity()
    # can make 10 chairs a day + extra day for packing
    days = quantity % 10 + 1
    return days


def write_message(ok):
    # update the html file with the number of days and message
    days = estimate_time()
    html_code = get_HTML_string("order_complete.html")
    if ok:
        html_code = html_code.replace(
            "MESSAGE",
            "<h2>Thank you for your order! </h2> <br> \
            <h3>We are very busy right now, but we aim to deliver your chair in "
            + str(days)
            + " days.</h3>",
        )
    if not ok:
        html_code = html_code.replace(
            "MESSAGE",
            "<h2>Your order could not be processed </h2> <br> \
            <h3>Please choose a new design.</h3>",
        )
    return html_code


def get_limit(max_or_min):
    # get limits from database
    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY = (
        '''
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT  ?name ?s_width ?s_depth ?a_th ?back_height ?top_th ?mid_th ?bot_th ?leg_height ?leg_th
            WHERE {
            ?a_chair a kbe:chair.
            ?a_chair kbe:name ?name.
            FILTER regex(?name, "'''
        + max_or_min
        + """") 
            ?a_chair kbe:s_width ?s_width.
            ?a_chair kbe:s_depth ?s_depth.
            ?a_chair kbe:a_th ?a_th.
            ?a_chair kbe:back_height ?back_height.
            ?a_chair kbe:top_th ?top_th.
            ?a_chair kbe:mid_th ?mid_th.
            ?a_chair kbe:bot_th ?bot_th.
            ?a_chair kbe:leg_height ?leg_height.
            ?a_chair kbe:leg_th ?leg_th.
            }
    """
    )
    PARAMS = {"query": QUERY}
    response = requests.post(URL, data=PARAMS)
    json_data = response.json()
    return json_data


def parse_json(json_data):  # returns an array with parameters
    chair_parms = {
        "name": 0,
        "s_width": 0,
        "s_depth": 0,
        "a_th": 0,
        "back_height": 0,
        "top_th": 0,
        "mid_th": 0,
        "bot_th": 0,
        "leg_height": 0,
        "leg_th": 0,
    }
    chair_list = []
    # get sizes
    num_of_chairs = len(json_data["results"]["bindings"])

    for x in range(num_of_chairs):
        for key in chair_parms:
            chair_parms[key] = json_data["results"]["bindings"][x][key]["value"]
        dic_copy = chair_parms.copy()
        chair_list.append(dic_copy)
    # print("Chair list",chair_list)
    return chair_list


def feedback_to_customer(values, min_list, max_list):
    # check if parameters are within limits
    ok = True
    for key in max_list[0]:
        if key == "name":
            continue
        if int(values[key]) > int(max_list[0][key]):
            ok = False
        elif int(values[key]) < int(min_list[0][key]):
            ok = False
    return ok


def add_chair(values):
    # add chair design to database
    values.pop("quantity")  # do not want to add quantity to chair class
    chair_name = str(values["s_width"]) + "x" + str(values["s_depth"])
    insert_str = (
        """kbe:chair_"""
        + chair_name
        + """ a kbe:chair.
                    kbe:chair_"""
        + chair_name
        + ''' kbe:name "'''
        + chair_name
        + """".\n"""
    )

    for key in values:

        if key.find("with") != -1:  # all boolean variables contain the word "with"
            datatype = "boolean"
        elif key.find("spindles") != -1:  # spindles is the only integer in the database
            datatype = "integer"
        else:
            datatype = "float"  # the rest of parameters are stored as floats
        insert_str += (
            "kbe:chair_"
            + chair_name
            + " kbe:"
            + key
            + ' "'
            + str(values[key])
            + '"^^xsd:'
            + datatype
            + ". \n"
        )

    URL = "http://127.0.0.1:3030/kbe/update"
    UPDATE = (
        """
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT
            {
             """
        + insert_str
        + """             
            }
            WHERE
            { 
            } 
            """
    )

    PARAMS = {"update": UPDATE}
    response = requests.post(URL, data=PARAMS)
    return chair_name


def add_order(chair_name, quantity, name, email):
    # add order to database
    orderID = name + chair_name

    URL = "http://127.0.0.1:3030/kbe/update"
    UPDATE = (
        """
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT
            {
             kbe:order_""" + orderID + """ a kbe:order. 
             kbe:order_""" + orderID + ''' kbe:name "''' + name + """".
             kbe:order_""" + orderID + ''' kbe:quantity "''' + str(quantity) + """"^^xsd:integer.
             kbe:order_""" + orderID + ''' kbe:email "''' + email + """".
             kbe:order_""" + orderID + """ kbe:status "0"^^xsd:boolean.            
            }
            WHERE
            { 
            }  
    """
    )
    PARAMS = {"update": UPDATE}
    response = requests.post(URL, data=PARAMS)


if __name__ == "__main__":
    customer_server = HTTPServer
    customer_httpd = customer_server((HOST_NAME, CUST_PORT_NUMBER), CustomerHandler)
    print(time.asctime(), "Customer Server - %s:%s" % (HOST_NAME, CUST_PORT_NUMBER))

    try:
        customer_httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    customer_httpd.server_close()
