"""
Team - Group 1
Members - Mahesh Kumaar Balaji (mbalaji@scu.edu), Narin Attaria (nattaria@scu.edu) , Chirag Radhakrishna (cradhakrishna@scu.edu), Shiva Kumar Reddy Rangapuram (srangapuram@scu.edu)
"""


import socket
import argparse
from payload import HTTPRequest, HTTPResponse


def recv_data_from_auctioneer(bidder_soc) -> str:
    recv_bytes = bidder_soc.recv(2048)
    return recv_bytes.decode()


def send_data_to_auctioneer(bidder_soc, request: str):
    bidder_soc.sendall(request.encode())


def make_request(request_type: str) -> str:
    httpRequest = None

    if request_type == "JOIN":
        httpRequest = HTTPRequest(args.host, args.port)
        httpRequest.make_request("JOIN")
    elif request_type == "BID":
        bid_amount = int(input("Enter BID Amount:"))
        httpRequest = HTTPRequest(args.host, args.port)
        httpRequest.make_request("BID", bid_amount=bid_amount)

    return str(httpRequest)


if __name__ == "__main__":
    bidder_socket = None
    try:
        argparser = argparse.ArgumentParser()
        argparser.add_argument("-p", "--port", type=int, action="store", help="Port Number to connect to", required=True)
        argparser.add_argument("-host", "--host", action="store", help="Host name or address of server to connect", default=socket.gethostname())
        args = argparser.parse_args()
        bidder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bidder_socket.connect((args.host, args.port))
        print(f"Bidder connected to the auction server - {args.host}:{args.port}.")
        request_string = make_request("JOIN")
        send_data_to_auctioneer(bidder_socket, request_string)
        print(f"'JOIN request sent to auction server for registration - {request_string}'")
        response_string = recv_data_from_auctioneer(bidder_socket)
        httpResponse = HTTPResponse()
        httpResponse.parse(response_string)
        if httpResponse.StatusCode != "200":
            print(f"Auction server returned an error while trying to register to the auction.")
            print(f"Response Status Message received - {httpResponse.StatusMessage}")
            print(f"Response body received: {httpResponse.Body}")
        else:
            print(f"Successfully registered to the auction. Status response received from auction server - {httpResponse.Body}")
            while True:
                user_ok_for_bid = input("Kindly confirm if you would like to place a BID (Y/N): ")
                if user_ok_for_bid.strip() == "Y":
                    request_string = make_request("BID")
                    print(f"Sending 'BID' request to the auction server. HTTP Request - {request_string}")
                    send_data_to_auctioneer(bidder_socket, request_string)
                    response_string = recv_data_from_auctioneer(bidder_socket)
                    httpResponse = HTTPResponse()
                    httpResponse.parse(response_string)
                    if httpResponse.StatusCode == "200":
                        print(f"BID has been successfully accepted by the auction.\nResponse received - {httpResponse.Body}")
                    else:
                        print(f"BID was rejected by the auction.\nResponse received - {httpResponse.Body}")
                else:
                    print(f"Waiting for broadcast messages.")
                    response_string = recv_data_from_auctioneer(bidder_socket)
                    httpResponse = HTTPResponse()
                    httpResponse.parse(response_string)
                    if httpResponse.StatusCode == "200":
                        print(f"Broadcast message received: {httpResponse.Body}")
                    else:
                        print(f"Error occurred while waiting for broadcast: {httpResponse.Body}")
    except Exception as ex:
        print(f"An error occurred while participating in the auction: {ex}")
    finally:
        if bidder_socket is not None:
            bidder_socket.close()
