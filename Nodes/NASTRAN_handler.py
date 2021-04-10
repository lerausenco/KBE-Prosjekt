from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from utils.parsers import  *
from os import curdir, sep
from utils.myHandler import myHandler


class NASTRAN_handler(myHandler):
    def do_GET(self):
        """
            Respond to a GET request.
            Images require their own file Content-type to be sent,
            so the send_image function is used to be able to display them.
        """
        #query fuseki and make model

        json_data = query_fuseki()
        node_list = parse_json(json_data)
        
        
        if not self.path.endswith(".png") and not self.path.endswith(".jpg") and not self.path.endswith(".gif"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("NASTRAN ready", "utf-8"))
            return
        else:
            self.send_image(self.path[-3])
            return
   
    def do_POST(self):

        """
            Respond to POST requests.
        """
        
        if not self.path.endswith(".png") and not self.path.endswith(".jpg") and not self.path.endswith(".gif"):
            
            #if not a picture, make text header
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_code = ""

            #check what text to write
            #User clicks Submit------------------
            if (self.path.find("params.php") != -1):
                html_code = get_HTML_string("UI\\customer_results.html")
                self.wfile.write(bytes(html_code, "utf-8"))
                param_line = self.get_params_from_path()
                values = parse_path(param_line)
                print("Values received: ", values)

                #update fuseki server

        else: #if image, make image header based on file type
            self.send_image(self.path[-3])
            return
                 

