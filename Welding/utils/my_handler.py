from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from utils.image_process import make_feedback, open_image, preprocess
from utils.space_for_welding_gun import find_space_for_welder
from utils.wall_extraction import extract_walls
import numpy as np
import time
import requests
import os
from os import curdir, sep
import sys

img_path = "img/maze3.png"

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

class myHandler(BaseHTTPRequestHandler):
    """
        Handles server requests
    """
    
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
        """
            Splits parameters from the rest of the path
            returns:
                param_line [string] - string containing parameters in key value pairs
        """

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
            time.sleep(1.5)
            self.send_image(self.path[-3])
            return

        
    def do_POST(self):

        """
            Respond to POST requests.
        """

        if not self.path.endswith(".png") and not self.path.endswith(".jpg"):
            
            #if not a picture, make text header
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_code = ""


            #check what text to write
            #User clicks Submit------------------
            if (self.path.find("weld_dims") != -1):
                html_code = get_HTML_string("UI/results.html")
                self.wfile.write(bytes(html_code, "utf-8"))
                param_line = self.get_params_from_path()
                values = parse_path(param_line)
                print("Values received: ", values)

                img = open_image(img_path)
                img_array = preprocess(img)

                #perform weldability check
                if (float(values['wall_height']) > float(values['gun_length'])/1000):
                    feedback_array = np.zeros(img_array.shape)
                    self.wfile.write(bytes("Your model is not weldable because the walls are too high.", "utf-8"))
                else:
                    feedback_array = find_space_for_welder(
                        img_array,
                        model_height=float(values['y_scale']),
                        model_length=float(values['x_scale']),
                        wall_height=float(values['wall_height']),
                        gun_diam=float(values['gun_diam']),
                        gun_length=float(values['gun_length'])
                        )

                #make feedback file
                make_feedback(feedback_array, img_array)
                print("picture made")

                #extract walls and write to txt file
                x_scale=float(values['x_scale'])/img.size[0]*1000*4
                y_scale=float(values['y_scale'])/img.size[1]*1000*4

                wall_list = extract_walls(img_array, 
                x_scale=x_scale,
                y_scale=y_scale,
                wall_height=float(values['wall_height'])*1000)

                max_x_length = x_scale * img.size[0]/4
                max_y_length = y_scale * img.size[1]/4

                #clear file
                f = open("param_vals.txt", "w").close()
                f = open("param_vals.txt", "a")
                f.write(str(max_x_length) + "\n") #y length
                f.write(str(max_y_length) + "\n") #x length
                for wall in wall_list:
                    f.write(str(wall.params()) + "\n")

                
            #------------------------------------------------------

            
            # User clicks Send results ----------------
            if (self.path.find("get_results") !=-1):
                param_line = self.get_params_from_path()
                customer_info = parse_path(param_line)

                customer_info['cust_email'] = customer_info['cust_email'].replace("%40", "@")
                html_code = ""
                html_code = get_HTML_string("UI/results.html")
                
                old = '''<input style=" height:40px; width:150px; " 
    type="submit" value="Send results" form=get_results >'''
                new =  '''Information sent to ''' + customer_info['cust_email'] + '''. Have a nice day!'''
                new_code = html_code.replace(old, new)
                self.wfile.write(bytes(new_code, "utf-8"))   

            #----------------------------------------------------
            # 
            # User clicks upload: 
            # image replaced with image defined in img_path     

            if (self.path.find("weld_geom") !=-1):
                #param_line = self.get_params_from_path()
                #print("params from upload", param_line)
                html_code = ""
                html_code = get_HTML_string("UI/home.html")
                new_code = html_code.replace('''src="UI/info_img.png"''', '''src="'''+img_path+'''"''')
                self.wfile.write(bytes(new_code, "utf-8"))

                return

        else: #if image, make image header based on file type
            self.send_image(self.path[-3])
            return
           

                    
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests """
