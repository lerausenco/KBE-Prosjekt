from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from utils.parsers import  *
from os import curdir, sep


class myHandler(BaseHTTPRequestHandler):
    """
        Handles server requests
    """
    
    def send_image(self, img_type):
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
            GET requests are dependent on what server is running and
            are defined in the child class.
        """
        pass
    def do_POST(self):

        """
            Respond to POST requests.
            POST requests are dependent on what server is running and
            are defined in the child class.
        """
        pass           

                    
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Handle requests """
