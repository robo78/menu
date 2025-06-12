#!/usr/bin/env python3
"""Simple menu to launch available server scripts.

Adds an option to display status of scripts that have been started
from this menu. Processes are launched in the background so multiple
servers can run concurrently."""
import subprocess
import os

SCRIPTS = {
    '1': 'esp_http_server.py',
    '2': 'esp_upload.py',
    '3': 'server.py',
    '4': 'server2.py',
}

# Track running processes {script_path: subprocess.Popen}
PROCESSES = {}


def main():
    while True:
        # clean up finished processes
        for script, proc in list(PROCESSES.items()):
            if proc.poll() is not None:
                PROCESSES.pop(script)

        print("\nAvailable options:")
        for key, script in sorted(SCRIPTS.items()):
            print(f" {key}) {script}")
        print(" s) Show status")
        print(" 0) Exit")

        choice = input("Select an option: ").strip().lower()
        if choice == '0':
            break
        if choice == 's':
            if not PROCESSES:
                print("No scripts launched from this menu.")
            else:
                for script, proc in PROCESSES.items():
                    status = "running" if proc.poll() is None else "stopped"
                    print(f"{script} - {status} (PID {proc.pid})")
            continue

        if choice in SCRIPTS:
            script = SCRIPTS[choice]
            existing = PROCESSES.get(script)
            if existing and existing.poll() is None:
                print(f"{script} is already running (PID {existing.pid})")
                continue

            cmd = ['python3', script]
            try:
                proc = subprocess.Popen(cmd)
                PROCESSES[script] = proc
                print(f"Started {script} with PID {proc.pid}")
            except Exception as exc:
                print(f"Error running {script}: {exc}")
        else:
            print("Invalid option")

if __name__ == '__main__':
    main()

