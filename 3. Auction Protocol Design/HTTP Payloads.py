"""
Team - Group 1
Members - Mahesh Kumaar Balaji (mbalaji@scu.edu), Narin Attaria (nattaria@scu.edu) , Chirag Radhakrishna (cradhakrishna@scu.edu), Shiva Kumar Reddy Rangapuram (srangapuram@scu.edu)
"""


import json


class HTTPRequest:
    def __init__(self, host: str, port: str):
        self.HTTPMethod = "POST"
        self.HTTPVersion = "HTTP/1.1"
        self.RequestPath = "/"
        self.Headers = dict()
        self.Body = dict()
        self.Host = host
        self.Port = port

    def __str__(self):
        RequestString = f"{self.HTTPMethod} {self.RequestPath} {self.HTTPVersion}\r\n"
        for header in self.Headers:
            RequestString += f"{header}: {self.Headers[header]}\r\n"
        RequestString += "\r\n"
        RequestString += json.dumps(self.Body)
        RequestString += "\r\n"

        return RequestString

    def make_request(self, RequestType: str, **args):
        if RequestType == "JOIN":
            self.Body.update({"request_type": "JOIN"})
        elif RequestType == "BID":
            self.Body.update({"request_type": "BID", "bid_amount": args["bid_amount"]})
        else:
            raise Exception("Invalid Request Type!")
        self.Headers.update({"Content-Type": "application/json", "Host": f"{self.Host}:{self.Port}"})
        self.Headers.update({"Content-Length": len(json.dumps(self.Body).encode())})

    def parse(self, request_string: str):
        request_string = request_string.strip("\r\n")
        Lines = request_string.split("\r\n")
        RequestLine = Lines[0]
        RequestLineParts = RequestLine.split(" ")
        self.HTTPMethod = RequestLineParts[0]
        self.RequestPath = RequestLineParts[1]
        self.HTTPVersion = RequestLineParts[2]
        for index in range(1, len(Lines) - 1):
            CurrentLine = Lines[index]
            CurrentLine = CurrentLine.strip()
            if CurrentLine == "":
                break
            HeaderKey = (CurrentLine.split(":")[0]).strip()
            HeaderValue = (CurrentLine.split(":")[1]).strip()
            self.Headers.update({HeaderKey: HeaderValue})

        RequestBody = Lines[len(Lines) - 1]
        self.Body = json.loads(RequestBody)

    def isvalid(self):
        if self.HTTPMethod != "POST":
            request_validity = False
        elif len(self.Headers) < 2:
            request_validity = False
        elif "Content-Type" not in self.Headers:
            request_validity = False
        elif "Content-Length" not in self.Headers:
            request_validity = False
        elif "Content-Type" in self.Headers and self.Headers["Content-Type"] != "application/json":
            request_validity = False
        elif len(json.dumps(self.Body).encode()) != int(self.Headers["Content-Length"]):
            request_validity = False
        else:
            request_validity = True

        return request_validity


class HTTPResponse:
    def __init__(self):
        self.HTTPVersion = "HTTP/1.1"
        self.StatusCode = str()
        self.StatusMessage = str()
        self.Headers = dict()
        self.Body = dict()

    def __str__(self):
        ResponseString = f"{self.HTTPVersion} {self.StatusCode} {self.StatusMessage}\r\n"
        for header in self.Headers:
            ResponseString += f"{header}: {self.Headers[header]}\r\n"
        ResponseString += "\r\n"
        ResponseString += json.dumps(self.Body)
        ResponseString += "\r\n"

        return ResponseString

    def make_response(self, ResponseType: str, **args):
        if ResponseType == "BAD_REQUEST":
            self.StatusCode = "403"
            self.StatusMessage = "BAD REQUEST"
        elif ResponseType == "AUCTION_NOT_OPEN":
            self.StatusCode = "409"
            self.StatusMessage = "AUCTION_NOT_OPEN"
        else:
            self.StatusCode = "200"
            self.StatusMessage = "OK"
        if len(args) > 0:
            self.Body.update({"request_type": ResponseType})
            for key in args:
                self.Body.update({key: args[key]})
        self.Headers.update({"Content-Type": "application/json"})
        self.Headers.update({"Content-Length": len(json.dumps(self.Body).encode())})

    def parse(self, response_string: str):
        response_string = response_string.strip("\r\n")
        Lines = response_string.split("\r\n")
        ResponseLine = Lines[0]
        ResponseLineParts = ResponseLine.split(" ")
        self.HTTPVersion = ResponseLineParts[0]
        self.StatusCode = ResponseLineParts[1]
        self.StatusMessage = ResponseLineParts[2]
        for index in range(1, len(Lines) - 1):
            CurrentLine = Lines[index]
            CurrentLine = CurrentLine.strip()
            if CurrentLine == "":
                break
            HeaderKey = (CurrentLine.split(":")[0]).strip()
            HeaderValue = (CurrentLine.split(":")[1]).strip()
            self.Headers.update({HeaderKey: HeaderValue})

        ResponseBody = Lines[len(Lines) - 1]
        self.Body = json.loads(ResponseBody)
