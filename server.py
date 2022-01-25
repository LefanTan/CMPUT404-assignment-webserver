#  coding: utf-8 
from cgitb import html
import socketserver
from urllib import response

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip().decode()
        print("---------------------------------------")
        # Print request headers
        print (self.data)

        request = self.data.split('\r\n')[0].split(' ')
        path = request[1]
        method = request[0]
        mimetype = "text/html"

        if(method != 'GET'):
            response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
        else: 
            try:
                if(path.endswith("/")):
                    path += "index.html"

                file = open("www" + path)

                if(path.endswith("html")):
                    mimetype = "text/html"
                elif(path.endswith("css")):
                    mimetype = "text/css"  

                response = 'HTTP/1.1 200 OK\r\nContent-Type: {0}; charset=utf-8\r\n\r\n'.format(mimetype) + file.read()
            except FileNotFoundError:
                response = 'HTTP/1.1 404 Not Found\r\nContent-Type: {0}; charset=utf-8\r\n\r\nFile {1} not found'.format(mimetype, path) 
            except IsADirectoryError:
                response = 'HTTP/1.1 301 Moved Permanently\r\nContent-Type: {0}; charset=utf-8\r\nLocation: {1}\r\n\r\nRedirecting'.format(mimetype, path + "/")

        self.request.sendall(response.encode())
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
