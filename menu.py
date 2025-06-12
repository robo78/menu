#!/usr/bin/env python3
"""Simple menu to launch available server scripts."""
import subprocess
import os

SCRIPTS = {
    '1': ('esp_http_server.py', 'esp_http_server.py'),
    '2': ('esp_upload.py', 'esp_upload.py'),
    '3': ('server.py', 'server.py'),
    '4': ('server2.py', 'server2.py'),
}


def main():
    while True:
        print("\nAvailable options:")
        for key, (script, _) in sorted(SCRIPTS.items()):
            print(f" {key}) {script}")
        print(" 0) Exit")
        choice = input("Select an option: ").strip()
        if choice == '0':
            break
        if choice in SCRIPTS:
            script = SCRIPTS[choice][0]
            cmd = ['python3', script]
            print(f"\nRunning {script}... (Ctrl+C to stop)\n")
            try:
                subprocess.run(cmd, check=True)
            except KeyboardInterrupt:
                print("\nStopped\n")
            except subprocess.CalledProcessError as exc:
                print(f"Error running {script}: {exc}")
        else:
            print("Invalid option")

if __name__ == '__main__':
    main()

