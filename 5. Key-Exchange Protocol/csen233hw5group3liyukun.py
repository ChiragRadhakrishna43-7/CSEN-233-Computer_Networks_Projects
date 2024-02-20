# CSEN 233 Homework 5 Group 3
# Key-Exchange Protocol Implementation
# Members: Yukun Li (yli26@scu.edu) & Chirag Radhakrishna (cradhakrishna@scu.edu)  
#--------------------------------------------------------------------------------

import socket
import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', filename = "csen233hw5group3liyukun.logs", filemode = "a")
logger = logging.getLogger(__name__)

p, q = 23, 5 # p and q are assumed to be agreed prior to the exchange.

def select_private_key(p): # choosing the secret key
    while True:
        try:
            a = int(input(f"Select private key b/w 1 and {p-1}: "))
            if 1<= a < p:
                logger.info(f"User has selected a private key a: {a}.")
                return a
            else:
                print("The private key must be b/w 1 and p-1.")
        except ValueError:
            print("Your private key must be an integer.")

def shared_secret(value,a,p):
    logger.info("User has obtained the information and is calculating the shared secret key.")
    return pow(value,a, p)

def key_exchange(connection, pr_key):
    A = pow(q, pr_key, p)
    logger.info("User has combined the private key with and p and q.")
    logger.info(f"Sending value {A} for shared secret calculation.")
    connection.send(str(A).encode())
    logger.info("Receiving information (B Value) for shared secret calculation.")
    B = int(connection.recv(1024).decode())
    logger.info(f"Partner's value: {B}")
    shared_secret_key = shared_secret(B, pr_key, p)
    logger.info(f"The shared secret calculated at this side is: {shared_secret_key}.")
    

def accept():
    partner_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = socket.gethostbyname(host)
    partner_addr = (addr, 0)
    partner_skt.bind(partner_addr)
    partner_skt.listen(1)
    logger.info('Starting to accept connection on {} port {}'.format(*partner_addr))
    print('Starting to accept connection on {} port {}'.format(partner_skt.getsockname()[0],partner_skt.getsockname()[1]))
    conn, addr = partner_skt.accept()
    try:
        logger.info(f"Connected with partner: {addr}.")
        secret = select_private_key(p)
        key_exchange(conn, secret)
    except Exception as e:
        logger.error(f"Error occured as follows: {e}.")
    finally:
        conn.close()

def connect(partner_addr, port_number):
    partner_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    partner_skt.connect((partner_addr, port_number))
    secret = select_private_key(p)
    key_exchange(partner_skt, secret)
    partner_skt.close()

def main():
    while True:
        mode = input("Select an option: (Accept/Connect): ").lower()
        if mode == "accept":
            logger.info("Accepting a connection from partner.")
            accept()
            break
        elif mode == "connect":
            address = input("Enter the address to connect to: ")
            port_number = int(input("Enter the port: "))
            connect(address, port_number)
            break
        else:
            print("Choose correct option.")
            continue

if __name__ == "__main__":
    main()
