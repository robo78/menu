#!/usr/bin/env python3
"""Simple menu to launch available server scripts.

Adds an option to display status of scripts that have been started
from this menu. Processes are launched in the background so multiple
servers can run concurrently."""
import subprocess
import os
from typing import Set

# File storing keys of scripts that should auto-start
AUTOSTART_FILE = "autostart.conf"

SCRIPTS = {
    '1': 'esp_http_server.py',
    '2': 'esp_upload.py',
    '3': 'server.py',
    '4': 'server2.py',
}

# Track running processes {script_path: subprocess.Popen}
PROCESSES = {}


def load_autostart() -> Set[str]:
    """Return set of script keys configured for auto-start."""
    if not os.path.exists(AUTOSTART_FILE):
        return set()
    with open(AUTOSTART_FILE) as f:
        return {line.strip() for line in f if line.strip() in SCRIPTS}


def save_autostart(auto: Set[str]) -> None:
    with open(AUTOSTART_FILE, "w") as f:
        for key in sorted(auto):
            f.write(f"{key}\n")


def manage_autostart(auto: Set[str]) -> None:
    """Interactively toggle which scripts should start automatically."""
    while True:
        print("\nAuto-start configuration:")
        for key, script in sorted(SCRIPTS.items()):
            mark = "[x]" if key in auto else "[ ]"
            print(f" {key}) {mark} {script}")
        print(" q) Back")
        choice = input("Toggle which script? ").strip().lower()
        if choice == 'q':
            save_autostart(auto)
            break
        if choice in SCRIPTS:
            if choice in auto:
                auto.remove(choice)
            else:
                auto.add(choice)
        else:
            print("Invalid option")


def main():
    autostart = load_autostart()

    # Automatically start configured scripts
    for key in sorted(autostart):
        script = SCRIPTS.get(key)
        if script:
            try:
                proc = subprocess.Popen(["python3", script])
                PROCESSES[script] = proc
                print(f"Auto-started {script} with PID {proc.pid}")
            except Exception as exc:
                print(f"Error auto-starting {script}: {exc}")

    while True:
        # clean up finished processes
        for script, proc in list(PROCESSES.items()):
            if proc.poll() is not None:
                PROCESSES.pop(script)

        print("\nAvailable options:")
        for key, script in sorted(SCRIPTS.items()):
            print(f" {key}) {script}")
        print(" s) Show status")
        print(" a) Configure auto-start")
        print(" 0) Exit")

        choice = input("Select an option: ").strip().lower()
        if choice == '0':
            break
        if choice == 's':
            if autostart:
                auto_list = ", ".join(SCRIPTS[k] for k in sorted(autostart))
                print(f"Auto-start: {auto_list}")
            else:
                print("Auto-start: none")

            if not PROCESSES:
                print("No scripts launched from this menu.")
            else:
                for script, proc in PROCESSES.items():
                    status = "running" if proc.poll() is None else "stopped"
                    print(f"{script} - {status} (PID {proc.pid})")
            continue

        if choice == 'a':
            manage_autostart(autostart)
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

