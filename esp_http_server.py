from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import os
from werkzeug.utils import secure_filename

UPLOAD_DIRS = {
    'upload': "/mnt/usbdrive/upload",
    'upload2': "/mnt/usbdrive/upload2"
}
MAX_SIZE = 10 * 1024 * 1024  # 10 MB

# Upewnij się, że katalogi istnieją
for dir_path in UPLOAD_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)

class UploadHandler(BaseHTTPRequestHandler):
    def _generate_filename(self):
        return datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"

    def _get_upload_dir(self):
        path_parts = [p for p in self.path.split('/') if p]
        if path_parts and path_parts[0] in UPLOAD_DIRS:
            return UPLOAD_DIRS[path_parts[0]]
        return UPLOAD_DIRS['upload']

    def _handle_upload(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            print(f"[DEBUG] Content-Length: {length}")
            print(f"[DEBUG] Headers:\n{self.headers}")

            if length > MAX_SIZE:
                raise ValueError(f"File too large (max {MAX_SIZE//(1024*1024)}MB)")

            upload_dir = self._get_upload_dir()

            # Nazwa pliku
            content_disp = self.headers.get('Content-Disposition', '')
            if 'filename=' in content_disp:
                filename = secure_filename(content_disp.split('filename=')[-1].strip('"\'')) or self._generate_filename()
            else:
                filename = self._generate_filename()

            if not filename.lower().endswith('.jpg'):
                filename = filename.rsplit('.', 1)[0] + '.jpg' if '.' in filename else filename + '.jpg'

            filepath_final = os.path.join(upload_dir, filename)
            filepath_temp = filepath_final + ".partial"

            # Stream write
            print(f"[{datetime.now()}] Receiving {filename} → {filepath_temp}")
            received = 0
            with open(filepath_temp, "wb") as f:
                while received < length:
                    chunk = self.rfile.read(min(4096, length - received))
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            if received != length:
                os.remove(filepath_temp)
                raise ValueError(f"Incomplete file ({received}/{length} bytes)")

            os.rename(filepath_temp, filepath_final)
            print(f"[OK] Saved: {filepath_final} ({received} bytes)")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        except Exception as e:
            print(f"[ERROR] {e}")
            self.send_response(500 if not isinstance(e, ValueError) else 400)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_PUT(self):
        self._handle_upload()

    def do_POST(self):
        self._handle_upload()

if __name__ == '__main__':
    print("\n[INFO] Dual Directory Upload Server")
    print(f"[INFO] Upload directories:")
    for name, path in UPLOAD_DIRS.items():
        print(f" - {name.ljust(8)} -> {path}")
    print(f"[INFO] Max file size: {MAX_SIZE//(1024*1024)}MB")
    print("[INFO] Listening on port 8080... (Ctrl+C to stop)\n")

    server = HTTPServer(('0.0.0.0', 8080), UploadHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped")
