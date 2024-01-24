# CSEN 233 HW-2
# Chirag Radhakrishna (cradhakrishna@scu.edu)
# --------------------------------------------------------------------------------------------

# HTTP-Client that connects to the desired server (here gaia.cs.umass.edu ) on port 80 using a TCP socket connection to request information about the authors.
# Utilized the logging library to understand potential errors (if exists) with the HTTP-Client code.


# Libraries:

import socket
import logging

# Implementation:

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def http_client_request(host, port, path="/"):
    try:
        logger.info(f"Connecting to the specified server: {host} on port {port}")
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock_cnn:

            sock_cnn.connect((host,port))
            logger.info("Connection established with the desired server.")

            http_req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
            logger.info(f"Sending the request:\n{http_req}")

            sock_cnn.sendall(http_req.encode())

            response = b""
            while True:
                data = sock_cnn.recv(1024)
                if not data:
                    break
                response = response + data
            logger.info("Received Response Successfully from the Server")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Connection Closed.")
        if sock_cnn:
            sock_cnn.close()


if __name__ == "__main__":
    server = "gaia.cs.umass.edu"
    port = 80
    path = "/kurose_ross/authors.php"
    http_client_request(server,port,path)
        
