from NASTRAN_handler import NASTRAN_handler
from utils.myHandler import ThreadedHTTPServer
import time
import argparse

#get arguments from command
parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default="localhost", help="Provide host name")
parser.add_argument("--port", type=int, default=4321, help="Provide port number")
args = parser.parse_args()


#run NASTRAN server
NASTRAN_server = ThreadedHTTPServer((args.host, args.port), NASTRAN_handler)
print(time.asctime(), "NASTRAN server running at %s:%s" % (args.host, args.port))

try:
    NASTRAN_server.serve_forever()          
except KeyboardInterrupt:

    NASTRAN_server.serve_close()
      
if __name__ == '__main__':
    main()
