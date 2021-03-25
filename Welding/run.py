import numpy as np
from utils.image_process import open_image, preprocess, make_feedback
from http.server import BaseHTTPRequestHandler, HTTPServer
from Wall import Wall
from utils.wall_extraction import extract_walls
from utils.my_handler import myHandler, ThreadedHTTPServer
import time
import argparse
import threading
from space_for_welding_gun import find_space_for_welder


#printing options for debugging
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=180)

img = open_image("img/maze.jpg")
img_array = preprocess(img)


feedback_array = find_space_for_welder(
    img_array,
    model_height=4,
    model_length=3,
    wall_height=2,
    gun_diam=400,
    gun_length=4)

make_feedback(feedback_array, img_array)

#wall_list = extract_walls(img_array)


#scaling_fac = 10
#f = open("param_vals.txt", "a")

#for wall in wall_list:
#    f.write(str(wall.params()) + "\n")


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