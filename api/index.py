from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/':
            response = {"message": "Hello World"}
        elif self.path == '/health':
            response = {"status": "healthy"}
        else:
            self.send_response(404)
            response = {"error": "Not Found"}
            
        self.wfile.write(json.dumps(response).encode())
        return 