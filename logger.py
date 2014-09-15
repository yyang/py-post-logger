#!/usr/bin/python

import BaseHTTPServer
import cgi
import logging
import logging.handlers
import json

# set up logger
LOG_FILENAME = 'analytics.out'

# set up handler and formatter
logger    = logging.getLogger('analytics')
handler   = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, 'D', 1, 0, None, False, False)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
# add formater and handler to logger
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# set up HTTP server
PORT = 4000

# set up HTTP request handler
class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        analytics_content = json.loads(post_body)
        if "analytics" in analytics_content:
            logger.info(analytics_content["analytics"])
        self.send_response(200)
# enable HTTP service
httpd = BaseHTTPServer.HTTPServer(('', PORT), ServerHandler)
print "Serving HTTP POST logger on port", PORT, "..."
httpd.serve_forever()
