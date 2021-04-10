import os
from os import curdir, sep
import sys
from datetime import datetime 
import requests


values = {
    "N_max": 0,
    "N_min": 0,
    "V_max": 0,
    "V_min": 0,
    "M_max": 0,
    "M_min": 0,
    "pipe_diam": 0,
    "wall_th":0
}




def parse_path(param_line):
    """
        Parses the path from the POST-request.
        args:
            param_line [string] - line to parse
        returns:
            values [dictionary] - dictionary of values containing wall dimensions
    """

    values = {}
    
    pairs = param_line.split("&")  # key value pairs

    for i in range(len(pairs)):
        param_value = pairs[i].split("=")[1]
        if param_value == "":
            values[pairs[i].split("=")[0]] = 0
        else:
            values[pairs[i].split("=")[0]] = param_value

    return values

def get_HTML_string(file_name):
    """
        Reads HTML file.
        args:
            file_name [string] - path to HTML file
        returns:
            f.read() [string] - contents of file 
    """


    f = open(os.path.join(sys.path[0], file_name), "r")
    return f.read()


def query_fuseki():
    # get limits from database
    URL = "http://127.0.0.1:3030/kbe/query"

    QUERY = """PREFIX kbe: <http://www.kbe.com/node.owl#>
            SELECT"""

    for key in values:
        QUERY += """?""" + key + """ """

    QUERY += """\nWHERE {
                ?a_node a kbe:Node.
                \n"""
    for key in values:
        QUERY += """?a_node kbe:"""+ key + """ ?""" + key + """.\n"""

    QUERY += "}" 
    
    print("QUERY--------", QUERY)

    PARAMS = {"query": QUERY}
    response = requests.post(URL, data=PARAMS)
    json_data = response.json()
    print(json_data)
    return json_data

def parse_json(json_data):  # returns an array with parameters

    node_list = []
    # get sizes
    num_of_nodes = len(json_data["results"]["bindings"])

    for x in range(num_of_nodes):
        for key in values:
            values[key] = json_data["results"]["bindings"][x][key]["value"]
        dic_copy = values.copy()
        node_list.append(dic_copy)
    print("Node list",node_list)
    return node_list

def update_fuseki(values):
    """
        Updates fuseki server with new node parameters.
        args:
            values - dictionary containing parameters from HTML form
        returns:
            response from server
    """
    
    #create ID-number from date and time
    now = datetime.now()
    ID = now.strftime('%d%m%y%H%M%S')
    node_name = str(ID)

    #create node
    insert_str = 'kbe:Node' + ID + ' a kbe:Node.\n'

    #extract values from dictionary
    for key in values:
        insert_str += "kbe:Node"+ ID + " kbe:" + key + ' "' + str(values[key]) + '"^^xsd:float. \n'

    URL = "http://127.0.0.1:3030/kbe/update"
    UPDATE = (
        """
            PREFIX kbe: <http://www.kbe.com/node.owl#>
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

    print("update query----- \n", UPDATE)
    PARAMS = {"update": UPDATE}
    response = requests.post(URL, data=PARAMS)
    print(response)
    return response