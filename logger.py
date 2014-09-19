#!/usr/bin/python

import os
import BaseHTTPServer
import json
import logging, logging.handlers

# logfile path and name
current_path = os.path.dirname(os.path.abspath(__file__));
log_filename = os.path.join('/edx/var/pseudo_analytics', 'analytics.log');

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
port  = 8001 
httpd = BaseHTTPServer.HTTPServer(('', port), ServerHandler)
httpd.serve_forever()

print "Serving HTTP POST logger on port", port, "..."
