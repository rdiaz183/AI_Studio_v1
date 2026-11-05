import os
import sys
import json
import winreg
import ctypes
import string
from datetime import datetime

TARGETS = {
    "VS Code": {"cmd": "code --version", "parser": lambda x: x.splitlines()[0]},
    "Git": {"cmd": "git --version", "parser": lambda x: x.strip()},
    "Python": {"cmd": "python --version", "parser": lambda x: x.strip()},
    "Ollama": {"cmd": "ollama --version", "parser": lambda x: x.strip()}
}

def get_logical_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

def locate_visual_studio():
    vswhere = r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
    if os.path.exists(vswhere):
        try:
            import subprocess
            res = subprocess.run([vswhere, "-latest", "-property", "installationPath"], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
    return "NOT_LOCATED"

def locate_unreal_engine(drives):
    # Method 1: Epic Games Launcher Manifest
    epic_dat = os.path.expandvars(r"%ProgramData%\Epic\UnrealEngineLauncher\LauncherInstalled.dat")
    if os.path.exists(epic_dat):
        try:
            with open(epic_dat, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("InstallationList", []):
                    app_name = item.get("AppName", "")
                    if app_name.startswith("UE_"):
                        bin_path = os.path.join(item.get("InstallLocation", ""), r"Engine\Binaries\Win64\UnrealEditor.exe")
                        if os.path.exists(bin_path):
                            return f"{app_name} ({bin_path})"
        except Exception:
            pass

    # Method 2: Multi-drive root scan
    for d in drives:
        for v in ["5.5", "5.4", "5.3", "5.2", "5.1", "5.0"]:
            candidates = [
                os.path.join(d, "Epic Games", f"UE_{v}", r"Engine\Binaries\Win64\UnrealEditor.exe"),
                os.path.join(d, "Program Files", "Epic Games", f"UE_{v}", r"Engine\Binaries\Win64\UnrealEditor.exe"),
                os.path.join(d, "UnrealEngine", f"UE_{v}", r"Engine\Binaries\Win64\UnrealEditor.exe"),
                os.path.join(d, "Games", "Epic Games", f"UE_{v}", r"Engine\Binaries\Win64\UnrealEditor.exe")
            ]
            for p in candidates:
                if os.path.exists(p):
                    return f"UE {v} ({p})"
    return "NOT_LOCATED"

def locate_blender(drives):
    for d in drives:
        # Check standard & Steam paths across all drives
        candidates = [
            os.path.join(d, r"Program Files\Blender Foundation"),
            os.path.join(d, r"SteamLibrary\steamapps\common\Blender"),
            os.path.join(d, r"Program Files (x86)\Steam\steamapps\common\Blender")
        ]
        for c in candidates:
            if os.path.exists(c):
                # Search for blender.exe directly or in subfolders
                for root, _, files in os.walk(c):
                    if "blender.exe" in files:
                        return os.path.join(root, "blender.exe")
    return "NOT_LOCATED"

def locate_godot(drives):
    for d in drives:
        candidates = [
            os.path.join(d, "Godot"),
            os.path.join(d, r"Program Files\Godot"),
            os.path.join(d, r"SteamLibrary\steamapps\common\Godot Engine")
        ]
        for c in candidates:
            if os.path.exists(c):
                for root, _, files in os.walk(c):
                    for f in files:
                        if f.lower().startswith("godot") and f.lower().endswith(".exe"):
                            return os.path.join(root, f)
    return "NOT_LOCATED"

def audit():
    import subprocess
    drives = get_logical_drives()
    report = {"timestamp": datetime.now().isoformat(), "cli_tools": {}, "engines": {}}

    print("\n--- AI_STUDIO v1: DEEP TOOLCHAIN & MULTI-DRIVE AUDIT ---")
    print(f"[*] Detected Logical Drives: {', '.join(drives)}")

    for name, item in TARGETS.items():
        try:
            res = subprocess.run(item["cmd"], capture_output=True, text=True, shell=True, timeout=5)
            report["cli_tools"][name] = item["parser"](res.stdout) if res.returncode == 0 else "MISSING"
        except Exception:
            report["cli_tools"][name] = "NOT_INSTALLED"
        status_flag = "[OK]" if report["cli_tools"][name] != "NOT_INSTALLED" else "[X]"
        print(f"{status_flag} {name:<20}: {report['cli_tools'][name]}")

    vs_path = locate_visual_studio()
    ue_path = locate_unreal_engine(drives)
    blender_path = locate_blender(drives)
    godot_path = locate_godot(drives)

    report["engines"]["Visual Studio"] = vs_path
    report["engines"]["Unreal Engine"] = ue_path
    report["engines"]["Blender"] = blender_path
    report["engines"]["Godot"] = godot_path

    print(f"{'[OK]' if vs_path != 'NOT_LOCATED' else '[!]'} {'Visual Studio':<20}: {vs_path}")
    print(f"{'[OK]' if ue_path != 'NOT_LOCATED' else '[!]'} {'Unreal Engine':<20}: {ue_path}")
    print(f"{'[OK]' if blender_path != 'NOT_LOCATED' else '[!]'} {'Blender':<20}: {blender_path}")
    print(f"{'[OK]' if godot_path != 'NOT_LOCATED' else '[!]'} {'Godot':<20}: {godot_path}")

    log_path = r"C:\Users\rdiaz\Documents\Unreal Projects\AI_Studio_Workspace\Workspace\Logs\toolchain_audit.json"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\n[OK] Deep Toolchain Telemetry logged to: {log_path}")

if __name__ == "__main__":
    audit()