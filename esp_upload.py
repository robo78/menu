# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from datetime import datetime

UPLOAD_DIR = "/mnt/usbdrive/upload"

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/upload':
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            path = os.path.join(UPLOAD_DIR, filename)
            with open(path, "wb") as f:
                f.write(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Upload OK")
            print("Saved file to:", path)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    server = HTTPServer(('0.0.0.0', 8080), UploadHandler)
    print("Server running on port 8080...")
    server.serve_forever()
