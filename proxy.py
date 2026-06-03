#!/usr/bin/env python3
"""
Serves the election dashboard and proxies the enhancedvoting API,
stripping Cross-Origin-Resource-Policy so browsers can read the response.
"""
import http.server
import urllib.request
import urllib.error
import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

API_URL = "https://app.enhancedvoting.com/results/public/api/elections/nevada-county-ca/2026StatewidePrimary/data"
BLOCKED_HEADERS = {"cross-origin-resource-policy", "cross-origin-opener-policy", "cross-origin-embedder-policy"}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/results":
            self.proxy_api()
        else:
            super().do_GET()

    def proxy_api(self):
        try:
            req = urllib.request.Request(API_URL, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, format, *args):
        pass  # suppress per-request logs

with http.server.HTTPServer(("", 8080), Handler) as httpd:
    print("Election dashboard: http://localhost:8080")
    httpd.serve_forever()
