"""
Team - Group 1
Members - Mahesh Kumaar Balaji (mbalaji@scu.edu), Narin Attaria (nattaria@scu.edu) , Chirag Radhakrishna (cradhakrishna@scu.edu), Shiva Kumar Reddy Rangapuram (srangapuram@scu.edu)
"""


import socket
import argparse
import logging
import datetime
import threading
import os
import time
from enum import Enum
from payload import HTTPRequest, HTTPResponse

lock = threading.Lock()
Auction_State = {
     "status": "OPEN",
     "highest_bid": 10,
     "highest_bidder": None,
     "chant": 0,
     "n_clients": list(),
     "next_auction": str(datetime.datetime.now() + datetime.timedelta(days=2)),
     "server_ip": None,
     "server_port": 8000,
     "broadcast_thread": None,
     "firstBidPlaced": False,
}


class LoggingLevel(Enum):
    ERROR = 1
    CRITICAL = 2
    INFO = 3


class Logging:
    @staticmethod
    def setConfiguration(LoggingMode: str) -> str:
        FileName = str()
        if LoggingMode == "f":
            # Logging Mode = 'f' writes the logs onto a newly generated log file.
            _CurrentTime = datetime.datetime.now()
            FileName = f"LogFile-{_CurrentTime.year}{_CurrentTime.month}{_CurrentTime.day}{_CurrentTime.hour}{_CurrentTime.minute}{_CurrentTime.second}{_CurrentTime.microsecond}.log"
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s  %(levelname)s %(lineno)d  %(message)s", datefmt="%d-%b-%y %H:%M:%S", encoding="utf-8", filename=FileName)
        else:
            # Any other values for Logging Mode writes the logs onto the console.
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s  %(levelname)s %(lineno)d %(message)s", datefmt="%d-%b-%y %H:%M:%S")

        return FileName

    @staticmethod
    def logentry(message: str, entry_level: LoggingLevel = LoggingLevel.INFO):
        if entry_level == LoggingLevel.ERROR:
            logging.error(message)
        elif entry_level == LoggingLevel.CRITICAL:
            logging.critical(message)
        else:
            logging.info(message)


def process_bidder(bidder_socket_param, bidder_address_param):
    Logging.logentry(f"Client - {bidder_address_param} has connected to the auction.")
    while True:
        try:
            client_request_string = recv_data_from_bidder(bidder_socket_param)
            Logging.logentry(f"Request received from client - {bidder_address_param}: {client_request_string}")
            httpRequest = HTTPRequest(Auction_State["server_ip"], str(Auction_State["server_port"]))
            httpRequest.parse(client_request_string)
            httpResponse = HTTPResponse()
            if Auction_State["status"] != "OPEN":
                httpResponse.make_response("AUCTION_NOT_OPEN", next_auction=Auction_State["next_auction"])
                Logging.logentry(f"Request received from {bidder_address_param[0]}, but as the auction is not yet open, a 'AUCTION_NOT_OPEN' response has been sent back to the bidder")
                Logging.logentry(f"Response sent back: {str(httpResponse)}")
            elif not httpRequest.isvalid():
                httpResponse.make_response("BAD_REQUEST", message="Format of HTTPRequest sent is invalid.")
                Logging.logentry(f"HTTP Request received is not valid, hence sending back a 'BAD_REQUEST' type response.", LoggingLevel.ERROR)
                Logging.logentry(f"Response sent back: {str(httpResponse)}", LoggingLevel.ERROR)
            else:
                request_body = httpRequest.Body
                if request_body["request_type"] == "JOIN":
                    with lock:
                        Auction_State["n_clients"].append((bidder_socket_param, bidder_address_param[0]))
                    httpResponse.make_response("STATUS", status=Auction_State["status"], highest_bid=Auction_State["highest_bid"], highest_bidder=Auction_State["highest_bidder"], chant=Auction_State["chant"], n_clients=len(Auction_State["n_clients"]), next_auction=Auction_State["next_auction"])
                    Logging.logentry(f"'JOIN' request received from {bidder_address_param[0]} and 'STATUS' response has been sent back to the bidder.")
                    Logging.logentry(f"Response sent back: {str(httpResponse)}")
                elif request_body["request_type"] == "BID":
                    BidAmount = int(httpRequest.Body["bid_amount"])
                    if BidAmount > Auction_State["highest_bid"]:
                        httpResponse.make_response("BID_ACK", bid_status="Your BID has been accepted.")
                        Logging.logentry(f"A valid bid received from {bidder_address_param[0]} and an acknowledgement has been sent back to the bidder.")
                        Logging.logentry(f"Response sent back: {str(httpResponse)}")
                        with lock:
                            Auction_State["highest_bid"] = BidAmount
                            Auction_State["highest_bidder"] = bidder_address_param[0]
                            Auction_State["chant"] = 0
                            if not Auction_State["firstBidPlaced"]:
                                Auction_State["firstBidPlaced"] = True
                                Auction_State["broadcast_thread"].start()
                    else:
                        httpResponse.make_response("BAD_REQUEST", message="You tried placing an invalid BID, so it has been rejected.")
                        Logging.logentry(f"An invalid bid was received from {bidder_address_param[0]} and a rejection response has been sent back to the bidder.")
                        Logging.logentry(f"Response sent back: {str(httpResponse)}")
                else:
                    httpResponse.make_response("BAD_REQUEST", message="You tried requesting for an invalid 'request_type'.")
                    Logging.logentry(f"An invalid 'request_type' was received from {bidder_address_param[0]} and a rejection response has been sent back to the bidder.")
                    Logging.logentry(f"Response sent back: {str(httpResponse)}")

            send_data_to_bidder(bidder_socket_param, httpResponse)
        except KeyboardInterrupt:
            break
        except Exception as ex1:
            Logging.logentry(f"Exception occurred while processing request from client - {bidder_address_param[0]}: {ex1}", LoggingLevel.CRITICAL)
            break
    Logging.logentry(f"Bidder {bidder_address_param[0]} has disconnected from the auction.")
    with lock:
        Auction_State["n_clients"].remove((bidder_socket_param, bidder_address_param[0]))
    bidder_socket_param.close()


def recv_data_from_bidder(bidder_soc: socket) -> str:
    recv_bytes = bidder_soc.recv(2048)
    return recv_bytes.decode()


def send_data_to_bidder(bidder_soc, response: HTTPResponse):
    bidder_soc.sendall(str(response).encode())


def send_broadcast_for_highest_bid():
    while True:
        time.sleep(10)
        httpResponse = HTTPResponse()
        if Auction_State["chant"] >= 3:
            Logging.logentry(f"3 broadcast messages with the highest BID has been sent out. So terminating the broadcast thread.")
            httpResponse.make_response("CLOSE", highest_bid=Auction_State["highest_bid"], highest_bidder=Auction_State["highest_bidder"])
            Logging.logentry(f"Broadcast response to be sent: {str(httpResponse)}")
            send_broadcast_message(httpResponse)
            with lock:
                Auction_State["status"] = "CLOSE"
            break
        else:
            httpResponse.make_response("BID_BROADCAST", highest_bid=Auction_State["highest_bid"], highest_bidder=Auction_State["highest_bidder"])
            Logging.logentry(f"Broadcast message to be sent: {str(httpResponse)}")
            send_broadcast_message(httpResponse)
            with lock:
                Auction_State["chant"] = Auction_State["chant"] + 1


def send_broadcast_message(response):
    bidders = Auction_State["n_clients"]
    for (bidder_soc_brd, bidder_addr_ip) in bidders:
        send_data_to_bidder(bidder_soc_brd, response)


if __name__ == "__main__":
    auctioneer_socket = None
    LogFileName = Logging.setConfiguration("f")

    try:
        argparser = argparse.ArgumentParser()
        argparser.add_argument("-s", "--server", action="store", help="Host name or IPv4 address of the Auctioneer", default=socket.gethostname())
        args = argparser.parse_args()
        auctioneer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        auctioneer_socket.bind((args.server, Auction_State["server_port"]))
        port_number = int(auctioneer_socket.getsockname()[1])

        if Auction_State["server_ip"] is None:
            Auction_State["server_ip"] = args.server
        if Auction_State["broadcast_thread"] is None:
            Auction_State["broadcast_thread"] = threading.Thread(target=send_broadcast_for_highest_bid)
        auctioneer_socket.listen(10)
        Logging.logentry(f"Auctioneer is listening at {args.server}:{port_number}.")
        print(f"Auctioneer is listening at {args.server}:{port_number}.")
        while True:
            bidder_socket, bidder_address = auctioneer_socket.accept()
            bidder_thread = threading.Thread(target=process_bidder, args=(bidder_socket, bidder_address))
            bidder_thread.start()
    except KeyboardInterrupt:
        Logging.logentry(f"Received 'QUIT' command. Closing the server now.")
    except Exception as ex:
        Logging.logentry(f"An exception occurred while processing bidder requests: {ex}", LoggingLevel.CRITICAL)
    finally:
        if auctioneer_socket is not None:
            auctioneer_socket.close()

    if LogFileName != str():
        print(f"Logs have been generated at the following location:\r\nFile Name: {LogFileName}\r\nDirectory: {os.getcwd()}")
