from customer_handler import customer_handler
from utils.myHandler import ThreadedHTTPServer
import time
import argparse



def main():

    #get arguments from command
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost", help="Provide host name")
    parser.add_argument("--port", type=int, default=1234, help="Provide port number")
    args = parser.parse_args()


    #run customer server
    customer_server = ThreadedHTTPServer((args.host, args.port), customer_handler)
    print(time.asctime(), "Customer server running at %s:%s" % (args.host, args.port))
 

    try:    
        customer_server.serve_forever()    
    except KeyboardInterrupt:
        customer_server.server_close()
     
    
if __name__ == '__main__':
    main()
