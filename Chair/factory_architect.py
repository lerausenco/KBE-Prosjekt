import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests


HOST_NAME = "localhost"
FACT_PORT_NUMBER = 2410


def get_html_string(file_name):
    f = open(os.path.join(sys.path[0], file_name), "r")
    return f.read()


class FactoryHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        str_path = self.path
        if str_path.find("/overview") != -1:
            chair_params = {
                "name": 0,
                "s_width": 0,
                "s_depth": 0,
                "a_th": 0,
                "with_arm": 0,
                "with_back": 0,
                "back_height": 0,
                "with_top": 0,
                "top_th": 0,
                "with_mid": 0,
                "mid_th": 0,
                "with_bot": 0,
                "bot_th": 0,
                "leg_height": 0,
                "leg_th": 0,
                "with_taper": 0,
                "spindles": 0,
            }
            order_params = {"name": 0, "quantity": 0, "email": 0, "status": 0}

            json_chair_data = make_query("chair", chair_params)
            chair_list = parse_json(json_chair_data, chair_params)
            json_order_data = make_query("order", order_params)
            order_list = parse_json(json_order_data, order_params)

            for i in range(len(chair_list)):
                make_DFA(chair_list[i])

            html_chair_data = order_overview(chair_list, order_list)
            html_code = get_html_string("factory_overview.html")
            html_code = html_code.replace("<p> No orders yet </p>", html_chair_data)
            self.wfile.write(bytes(html_code, "utf-8"))

        if str_path.find("/set_limits") != -1:

            # page to set limits
            html_code = get_html_string("factory_setLimits.html")
            self.wfile.write(bytes(html_code, "utf-8"))

        if str_path.find("/max_limits") != -1:

            max_values = {}

            html_code = get_html_string("factory_setLimits.html")
            # let the user know they have been updated
            html_code = html_code.replace(
                '<input type="submit" value="Set Max Limits">',
                "Max limits have been updated",
            )
            self.wfile.write(bytes(html_code, "utf-8"))

            str_path = str_path.replace("+", "_")
            data = str_path.split("?")
            params = data[1]
            pairs = params.split("&")  # key value pairs

            for i in range(len(pairs)):
                param_value = pairs[i].split("=")[1]
                if param_value == "":
                    max_values[pairs[i].split("=")[0]] = 0
                else:
                    max_values[pairs[i].split("=")[0]] = param_value

            set_limits("MAX", max_values)

        if str_path.find("/min_limits") != -1:

            min_values = {}

            html_code = get_html_string("factory_setLimits.html")
            # let the user know they have been updated
            html_code = html_code.replace(
                '<input type="submit" value="Set Min Limits">',
                "Min limits have been updated",
            )
            self.wfile.write(bytes(html_code, "utf-8"))

            str_path = str_path.replace("+", "_")
            data = str_path.split("?")
            params = data[1]
            pairs = params.split("&")  # key value pairs

            for i in range(len(pairs)):
                param_value = pairs[i].split("=")[1]
                if param_value == "":
                    min_values[pairs[i].split("=")[0]] = 0
                else:
                    min_values[pairs[i].split("=")[0]] = param_value

            set_limits("MIN", min_values)


def set_limits(max_or_min, values):
    # add a chair_MAX for max limits and a chair_MIN for min limits

    insert_str = (
        """kbe:chair_""" + max_or_min + """ a kbe:chair. \n
            kbe:chair_"""+ max_or_min + ''' kbe:name "''' + max_or_min + """".\n"""
    )

    for key in values:
        insert_str += ("kbe:chair_" + max_or_min + " kbe:" + key + ' "' + str(values[key]) + '"^^xsd:float. \n')
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


def parse_json(json_data, dictionary):  # returns an array with parameters
    chair_list = []
    # get sizes
    num_of_chairs = len(json_data["results"]["bindings"])
    for x in range(num_of_chairs):
        for key in dictionary:
            dictionary[key] = json_data["results"]["bindings"][x][key]["value"]
        dic_copy = dictionary.copy()
        chair_list.append(dic_copy)
    # print("Chair list",chair_list)
    return chair_list


def make_query(class_name, dictionary):

    where_str = "?a_" + class_name + " a kbe:" + class_name + ".\n"
    select_str = ""
    for key in dictionary:
        select_str += " ?" + key
        where_str += " ?a_" + class_name + " kbe:" + key + "" " ?" + key + ". \n"

    URL = "http://127.0.0.1:3030/kbe/query"
    QUERY = (
        """
            PREFIX kbe: <http://www.kbe.com/chairs.owl#>
            SELECT """
        + select_str
        + """
            WHERE {
               """
        + where_str
        + """
            }
            """
    )
    print("QUERY::", QUERY)
    PARAMS = {"query": QUERY}
    response = requests.post(URL, data=PARAMS)
    print("Result of query:", response.text)
    json_order_data = response.json()
    # print("JSON", json_data)
    return json_order_data


def order_overview(chair_list, order_list):

    msg = ""
    for x in range(len(chair_list)):
        msg += "<tr>"
        # for key in chair_list[x]:
        msg += (
            "<td>" + chair_list[x]["name"] + "</td>"
            "<td>" + order_list[x]["name"] + "</td>"
            "<td>" + order_list[x]["email"] + "</td>"
            "<td>" + order_list[x]["quantity"] + "</td>"
            "<td>" + order_list[x]["status"] + "</td>"
        )
        msg += "</tr>"

    return msg


def make_DFA(chair):

    # access base template
    template_path = "DFA\\Templates\\Chair_base.dfa"
    f = open(template_path, "r")
    dfa_txt = f.read()

    # if file with chair name does not exist, make one
    if not os.path.isfile("DFA\\Orders\\" + chair["name"] + ".dfa"):

        # create new dfa file with chair name
        order_dfa = open("DFA\\Orders\\" + chair["name"] + ".dfa", "w")

        # write number parameters into dfa file
        for key in chair:
            dfa_txt = dfa_txt.replace("<" + key + ">", chair[key])

        order_dfa.write(dfa_txt)

        if chair["with_arm"] != "0":
            feature_file = open("DFA\\Templates\\arm_support.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if chair["with_back"] != "0":
            feature_file = open("DFA\\Templates\\Back.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if chair["with_top"] != "0":
            feature_file = open("DFA\\Templates\\rail-top.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if chair["with_mid"] != "0":
            feature_file = open("DFA\\Templates\\rail-mid.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if chair["with_bot"] != "0":
            feature_file = open("DFA\\Templates\\rail-bot.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if chair["with_taper"] != "0":
            feature_file = open("DFA\\Templates\\taper.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if int(chair["spindles"]) > 0:
            feature_file = open("DFA\\Templates\\spindles.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if int(chair["spindles"]) > 2:
            feature_file = open("DFA\\Templates\\spindles3.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        if int(chair["spindles"]) > 3:
            feature_file = open("DFA\\Templates\\spindles4.txt", "r")
            feature_txt = feature_file.read()
            order_dfa.write(feature_txt)

        order_dfa.close()


if __name__ == "__main__":
    factory_server = HTTPServer
    factory_httpd = factory_server((HOST_NAME, FACT_PORT_NUMBER), FactoryHandler)
    print(time.asctime(), "Factory Server - %s:%s" % (HOST_NAME, FACT_PORT_NUMBER))

    try:
        factory_httpd.serve_forever()

    except KeyboardInterrupt:
        pass

    factory_httpd.server_close()
