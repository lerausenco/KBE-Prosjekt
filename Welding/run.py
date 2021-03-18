import numpy as np
from utils.image_process import open_image, preprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from Wall import Wall
from utils.wall_extraction import extract_walls
from utils.my_handler import myHandler, ThreadedHTTPServer
import time
import argparse
import threading


#printing options for debugging
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=180)

#img = open_image('img/maze.png')
#img_array = preprocess(img)

#wall_list = extract_walls(img_array)


scaling_fac = 10
#f = open("param_vals.txt", "a")

#for wall in wall_list:
 #   f.write(str(wall.params()) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost", help="Provide host name")
    parser.add_argument("--port", type=int, default=1024, help="Provide port number")

    args = parser.parse_args()

    #customer_server = HTTPServer
    #customer_httpd = customer_server((args.host, args.port), myHandler)
    server = ThreadedHTTPServer((args.host, args.port), myHandler)
    print(time.asctime(), "Server running at %s:%s" % (args.host, args.port))

    try:
        
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    server.server_close()

    


if __name__ == '__main__':
    main()
