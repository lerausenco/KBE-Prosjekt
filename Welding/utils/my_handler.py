from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import time
import requests
import os
from os import curdir, sep
import sys

#import weld_geom
from get_image_from_website import mainfunc

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
            html_code = ""
            html_code = get_HTML_string("UI/results.html")
            old = '''<hr>
                    Provide contact information to receive a copy by email. 
                    <form id=get_results action="/get_results.php" method="POST">  
                    <label for="cust_name"><b>Name</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label><br>
                    <input type="text" class = "textbox" id="cust_name" name="cust_name">  <br><br>
                    <label for="cust_email"><b>Email</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label><br>
                    <input type="text" id="cust_email" name="cust_email"> <br><br>
                    <div style="text-align:right;">
                    <input style=" height:40px; width:150px; "     
                    type="submit" value="Send results" form=get_results >  '''
            new =  ''' <hr>
                    Information sent. Have a nice day!  '''
            html_code.replace(old,new)
            self.wfile.write(bytes(html_code, "utf-8"))

  #      if self.path.find("weld_geom") !=-1:
   #         print("found weld geom")
   #         self.send_response(200)
   #         self.send_header("Content-type", "text/html")
   #         self.end_headers()
   #         html_code = get_HTML_string("UI/home.html")
   #         self.wfile.write(bytes(html_code, "utf-8"))
           # url = "http://localhost:1024/weld_geom.php"
            #mainfunc(url, "Uploaded_images")
            #print("image upploaded ")
        

        
            
            


            

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests """