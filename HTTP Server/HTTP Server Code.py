# CSEN 233 MIDTERM
# Chirag Radhakrishna (cradhakrishna@scu.edu)
#--------------------------------------------
# MIDTERM OPEN QUESTION: Simple HTTP Server.
# The server accepts a single request from a web browser. Used Google Chrome as the test browser.
#------------------------------------------------------------------------------------------------

# Libraries
import socket
import logging
import random

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s -%(message)s', filename = "csen233midtermRadhakrishnaChirag.logs", filemode = "w")
logger = logging.getLogger(__name__)


def http_server(port_number):
    ARBITRARY_DATA = "Top 5 NBA players: 1.Michael Jordan 2.Lebron James 3.Kobe Bryant 4.Stephen Curry 5.Shaq"

    serverSKT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    serverSKT.bind(('', port_number))
    serverSKT.listen(1)
    server_addr = ('localhost',port_number)

    logger.info("Server has been started. Waiting for connection....")
    logger.info("Server is accepting single request.")
    logger.info(f"Server Address is http://{server_addr[0]}:{server_addr[1]}")
    print(f"Server Address is http://{server_addr[0]}:{server_addr[1]}")

    while True:
        clientSKT, client_addr = serverSKT.accept()
        logger.info(f"Browser {client_addr} has established a connection with the server")
        try:
            message = clientSKT.recv(1024).decode()
            logger.info(f"Received a GET request message from client: {client_addr}")
            logger.info(f"Request received is:\n {message}")
            random_number = random.random()
            if random_number < 0.5:
                    response_status = "HTTP/1.1 404 Not Found\r\n"
                    response_data = "404 Not Found. Cannot Display Data. This error message is displayed on purpose"
            else:
                response_status = "HTTP/1.1 200 OK\r\n"
                response_data = ARBITRARY_DATA
            response_message = response_status + "\r\n" + response_data
            logger.info("Constructing the response message which includes the HTTP headers and the response data.")
            logger.info(f"Response is {response_message}")
            clientSKT.send(response_message.encode())
        except Exception as e:
            logger.error(f"Error in establishing connection with client {client_addr}. Error was: {e}")
        finally:
            clientSKT.close()
            logger.info("Closing the client connection")
            logger.info("-------------------------------------------------------------------------")

if __name__ == "__main__":
    port = 43437
    http_server(port)
       

