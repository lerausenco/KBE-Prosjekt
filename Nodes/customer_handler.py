from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from utils.parsers import  *
from os import curdir, sep
from utils.myHandler import myHandler
import time
import os
import glob
import pathlib


class customer_handler(myHandler):

    def get_newest_gif(self):

        """
            Get gif file for simulation.
            ret:
                latest_file [string] - Path to latest file.
        """

        gif_path = "Gif\\*.gif" 
        latest_file = max(glob.glob(gif_path), key=os.path.getmtime)
        latest_file = latest_file.replace("\\", "/")
        print("Latest file ", latest_file)
        return latest_file
        
    
    def get_second_newest_gif(self):
        """
            Get gif file for simulation.
            ret:
                latest_file [string] - Path to latest file.
        """

        gif_path = "Gif\\*.gif" 
        latest_file = sorted(glob.glob(gif_path), key=os.path.getmtime)[-2]
        latest_file = latest_file.replace("\\", "/")
        print("Latest file ", latest_file)
        return latest_file
        


    def get_material(self):

        """
            Gets recommended material.
            ret:
                recommended material [string]
        """

        f = open("params.txt", "r")
        text = f.read()
        text = text.replace("'","")
        text = text.replace(" ", "")
        text = text.replace("{","")
        text = text.replace("}", "")

        param_pairs = text.split(",")

        param_dict = {}

        for param_pair in param_pairs:
            param_name = param_pair.split(":")[0]
            param_val = param_pair.split(":")[1]

            param_dict[param_name] = param_val

        return param_dict["material_pref"]

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
            html_code = get_HTML_string("UI\\customer_results.html")

            #get gifs
            latest_file = self.get_newest_gif()
            html_code = html_code.replace("GIF_FILE_PATH_MAX", latest_file)
            second_latest = self.get_second_newest_gif()
            html_code = html_code.replace("GIF_FILE_PATH_MIN", second_latest)

            #get material
            material = self.get_material()
            html_code = html_code.replace("STRENGTH_MATERIAL1", material)

            #print(html_code) #debugging

            #check what text to write
            #User clicks Submit------------------
            if (self.path.find("params.php") != -1):
                #update fuseki server 
                param_line = self.get_params_from_path()
                values = parse_path(param_line)
                print("Values received: ", values)
                update_fuseki(values)

                #display results
                
                self.wfile.write(bytes(html_code, "utf-8"))
                
        else: #if image, make image header based on file type
            self.send_image(self.path[-3])
            return
                 

