from http.server import BaseHTTPRequestHandler
import urllib.request
import json

UPSTREAM = "https://app.enhancedvoting.com/results/public/api/elections/nevada-county-ca/2026StatewidePrimary/data"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            req = urllib.request.Request(UPSTREAM, headers={"Accept": "application/json"})
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
