# server.py - Flask serwer HTTP przyjmujący zdjęcia przez PUT
# -*- coding: utf-8 -*-

from flask import Flask, request, abort
import os
from datetime import datetime

UPLOAD_DIR = "/mnt/usbdrive/upload"

app = Flask(__name__)
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/upload/<filename>", methods=["PUT"])
def upload(filename):
    try:
        data = request.get_data()
        size = len(data)
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            f.write(data)
        print(f"? Zapisano: {path} ({size} bajtów)")
        return "OK", 200
    except Exception as e:
        print(f"? Błąd zapisu: {e}")
        return "Błąd", 500

if __name__ == "__main__":
    print(f"Serwer startuje na porcie 8080...")
    app.run(host="0.0.0.0", port=8080)
