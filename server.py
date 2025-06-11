# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
from datetime import datetime

# �cie�ki do folder�w
UPLOAD_DIR = "/mnt/usbdrive/upload"
UPLOAD2_DIR = "/mnt/usbdrive/upload2"

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Sprawd� kt�ry endpoint zosta� wywo�any
        if self.path in ['/upload', '/upload2']:
            try:
                # Odczytaj d�ugo�� zawarto�ci
                content_length = int(self.headers['Content-Length'])
                
                # Okre�l folder docelowy na podstawie endpointu
                target_dir = UPLOAD2_DIR if self.path == '/upload2' else UPLOAD_DIR
                
                # Utw�rz folder je�li nie istnieje
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Odczytaj dane
                file_data = self.rfile.read(content_length)

                # Generuj unikaln� nazw� pliku
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}.jpg"
                #file_name = f"{timestamp}_{os.urandom(4).hex()}.jpg"  # Dodaj losowy suffix dla unikalno�ci
                file_path = os.path.join(target_dir, file_name)

                # Zapisz plik
                with open(file_path, "wb") as f:
                    f.write(file_data)

                # Odpowied� sukcesu
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"File uploaded successfully!")
                print(f"Saved file to {file_path}")  # Logowanie na serwerze

            except Exception as e:
                # Obs�uga b��d�w
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
                print(f"Error handling upload: {e}")

        else:
            # Nieznany endpoint
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found!")

if __name__ == "__main__":
    # Utw�rz foldery je�li nie istniej�
    for directory in [UPLOAD_DIR, UPLOAD2_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

    # Konfiguracja serwera � nas�uchiwanie na wszystkie interfejsy
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, UploadHandler)
    
    print(f"Server running on port 8080...")
    print(f"Main upload directory: {UPLOAD_DIR}")
    print(f"Secondary upload directory: {UPLOAD2_DIR}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

