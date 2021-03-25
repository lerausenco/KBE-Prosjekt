import numpy as np
from utils.my_handler import myHandler, ThreadedHTTPServer
import time
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost", help="Provide host name")
    parser.add_argument("--port", type=int, default=1024, help="Provide port number")
    parser.add_argument("--img", type=str, default="img/maze.png", help="Provide file path")
    args = parser.parse_args()


    server = ThreadedHTTPServer((args.host, args.port), myHandler)
    print(time.asctime(), "Server running at %s:%s" % (args.host, args.port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    server.server_close()

if __name__ == '__main__':
    main()
