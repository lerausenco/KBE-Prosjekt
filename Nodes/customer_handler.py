from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from utils.parsers import  *
from os import curdir, sep
from utils.myHandler import myHandler


class customer_handler(myHandler):
    def do_GET(self):
        """
            Respond to a GET request.
            Images require their own file Content-type to be sent,
            so the send_image function is used to be able to display them.
        """

        
        if not self.path.endswith(".png") and not self.path.endswith(".jpg") and not self.path.endswith(".gif"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_code = get_HTML_string("UI\\customer_params.html")
            self.wfile.write(bytes(html_code, "utf-8"))
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

                #update fuseki server 
                param_line = self.get_params_from_path()
                values = parse_path(param_line)
                print("Values received: ", values)
                update_fuseki(values)

                #display results
                html_code = get_HTML_string("UI\\customer_results.html")
                self.wfile.write(bytes(html_code, "utf-8"))
                

        else: #if image, make image header based on file type
            self.send_image(self.path[-3])
            return
                 

