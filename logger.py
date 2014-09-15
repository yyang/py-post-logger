#!/usr/bin/python

import ConfigParser
import os
import BaseHTTPServer
import json
import logging, logging.handlers

# config files
config = ConfigParser.ConfigParser()
config.read("config.ini")

# logfile path and name
current_path = os.path.dirname(os.path.realpath(__file__));
log_filename = os.path.join(current_path,
                            config.get('py_logger', 'log_path'),
                            config.get('py_logger', 'log_filename'))

# logger and handler
logger    = logging.getLogger('analytics')
handler   = logging.handlers.TimedRotatingFileHandler(log_filename, 'D', 1, 0, None, False, False)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# http handler
class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(400)
        self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        try:
            analytics_content = json.loads(post_body)
            if "analytics" in analytics_content:
                logger.info(analytics_content["analytics"])
            self.send_response(200)
        except (ValueError, RuntimeError, TypeError, NameError):
            self.send_response(400)
        self.end_headers()

# enable HTTP service
port  = config.getint('py_logger', 'port')
httpd = BaseHTTPServer.HTTPServer(('', port), ServerHandler)
httpd.serve_forever()

print "Serving HTTP POST logger on port", port, "..."
