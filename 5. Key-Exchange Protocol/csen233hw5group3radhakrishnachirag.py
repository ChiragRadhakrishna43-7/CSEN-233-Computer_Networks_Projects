# CSEN 233 Homework 5 Group 3
# Key-Exchange Protocol Implementation

# Members: Chirag Radhakrishna (cradhakrishna@scu.edu) and Yukun Li (yli26@scu.edu)
#----------------------------------------------------------------------------------

import socket
import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', filename = "csen233hw5group3radhakrishnachirag.logs", filemode = "a")
logger = logging.getLogger(__name__)

p, q = 23, 5 # shared public key

def select_secret(p): #pick secret key
    while True:
        try:
            b = input(f"Select a private key from 1 to {p-1}: ")
            b = int(b)
            if b in range(1,p):
                logger.info(f"User's private key is {b}.")
                return b
            else:
                print(f"Key should be in range 1 to {p-1}.")
        except ValueError:
            print("Secret key should be an integer.")
    

def shared_secret_calcn(info, b, p):
    logger.info("Compute shared secret key with partner's information.")
    return pow(info, b, p)

def diffie_hellman_ke(conn, scr_key):
    B = pow(q, scr_key,p)
    logger.info(f"Computed and sending value B: {B} to partner for secret key calculation.")
    conn.send(str(B).encode())
    A = float(conn.recv(1024).decode())
    logger.info(f"Received information for calculating the shared secret key.")
    logger.info(f"Value received- {A}")
    shared_secret = shared_secret_calcn(int(A), scr_key, p)
    logger.info(f"Shared secret key determined is: {shared_secret}.")

def accept():
    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    partner_address = socket.gethostbyname(socket.gethostname())
    address = (partner_address, 0)
    accept_socket.bind(address)
    port = accept_socket.getsockname()[1]
    logger.info('{} accepting connection on port {}'.format(accept_socket.getsockname()[0], port))
    print('{} accepting connection on port {}'.format(accept_socket.getsockname()[0], port))
    accept_socket.listen(1)

    conn, addr = accept_socket.accept()
    try:
        logger.info(f"Received connection from: {addr}.")
        b = select_secret(p)
        diffie_hellman_ke(conn, b)
    except Exception as e:
        logger.error(f"Error is as follows:{e}.")
    finally:
        conn.close()

def connect(addr, port_number):
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.info(f"Connecting with {addr} on port {port_number}.")
    connection_socket.connect((addr, port_number))
    b = select_secret(p)
    diffie_hellman_ke(connection_socket,b)
    connection_socket.close()

if __name__ == "__main__":
    while True:
        choice = input("Enter accept or connect: ").lower()
        if choice == "accept":
            logger.info("Partner is connecting.")
            accept()
            break
        elif choice == "connect":
            addr = input("Enter the partner's address: ")
            port = int(input("Mention the port number: "))
            connect(addr,port)
            break
        else:
            print("Enter either accept or connect.")
            continue
