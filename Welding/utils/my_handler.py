from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import time
import requests
import os
from os import curdir, sep
import sys


def parse_path(param_line):
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
    f = open(os.path.join(sys.path[0], file_name), "r")
    return f.read()

class myHandler(BaseHTTPRequestHandler):

    def send_image(self,img_type):
        """
            Creates the correct header for image type.
            args:
                img_type [string] - file ending for image 
        """
        f = open(curdir + sep + self.path, 'rb')
        self.send_response(200)
        self.send_header("Content-type","image/"+img_type)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
    
    def get_params_from_path(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        param_line = post_body.decode()
        return param_line
    
    def do_HEAD(self):
        """
            Serves the HEAD request type.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """
            Respond to a GET request.
            Images require their own file Content-type to be sent,
            so the send_image function is used to be able to display them.
        """
        if not self.path.endswith(".png") and not self.path.endswith(".jpg"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_code = get_HTML_string("UI/home.html")
            self.wfile.write(bytes(html_code, "utf-8"))
            return
        else:
            self.send_image(self.path[-3])
            return

        
    def do_POST(self):

        if not self.path.endswith(".png") and not self.path.endswith(".jpg") :
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_code = ""
            html_code = get_HTML_string("UI/results.html")
            self.wfile.write(bytes(html_code, "utf-8"))
            
        else:
            self.send_image(self.path[-3])
            

        if self.path.find("weld_dims") != -1:
            param_line = self.get_params_from_path()
            values = parse_path(param_line)
            print("Values received: ", values)

        if self.path.find("get_results") !=-1:
            param_line = self.get_params_from_path()
            customer_info = parse_path(param_line)
            print("Customer info: ", customer_info)
            
            


            

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests """