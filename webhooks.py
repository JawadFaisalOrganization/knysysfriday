#!/usr/bin/env python
#-*- coding:utf-8 -*-

import BaseHTTPServer
import sys
import time
import urlparse
import json
import socket

import os
import socket
import datetime
import copy



HOST_NAME =  'huresys.com'
PORT_NUMBER = int('5000')
# http_host = request.env.http_host.split(':')[0]
# print 'socket name'
# print socket.gethostbyname(http_host)
# hosts = (http_host, socket.gethostname(),
#              socket.gethostbyname(http_host),
#              '::1', '127.0.0.1', '::ffff:127.0.0.1')
# print 'host'  
print hosts           


def handle_hook(payload):
    pass


class HookHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    server_version = "HookHandler/0.1"
    def do_GET(s):
        s.send_response(200)
        s.wfile.write('Hello!')

    def do_POST(s):
        # Check that the IP is within the GH ranges
        if not any(s.client_address[0].startswith(IP)
                   for IP in ('192.30.252', '192.30.253', '192.30.254', '192.30.255')):
            s.send_error(403)
        print s
        length = int(s.headers['Content-Length'])
        post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
        print post_data
        payload = json.loads(post_data['payload'][0])

        handle_hook(payload)

        s.send_response(200)


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), HookHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)