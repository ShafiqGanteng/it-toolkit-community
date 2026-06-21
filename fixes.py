import os
import subprocess
import time
from colors import Colors


def fix_audio():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[FIX AUDIO]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    try:
        subprocess.run(["net", "stop", "audiosrv"], capture_output=True)
        time.sleep(2)
        subprocess.run(["net", "start", "audiosrv"], capture_output=True)
        subprocess.run(["net", "stop", "AudioEndpointBuilder"], capture_output=True)
        time.sleep(2)
        subprocess.run(["net", "start", "AudioEndpointBuilder"], capture_output=True)
        subprocess.Popen(["msdt.exe", "/id", "AudioPlaybackDiagnostic"])
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Audio fix complete!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def fix_bluetooth():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[FIX BLUETOOTH]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    try:
        subprocess.run(["net", "stop", "bthserv"], capture_output=True)
        time.sleep(2)
        subprocess.run(["net", "start", "bthserv"], capture_output=True)
        subprocess.Popen(["msdt.exe", "/id", "BluetoothDiagnostic"])
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Bluetooth fix complete!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def fix_windows_update():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[FIX WINDOWS UPDATE]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    try:
        services = ["wuauserv", "cryptSvc", "bits", "msiserver"]
        for svc in services:
            subprocess.run(["net", "stop", svc], capture_output=True)
        
        for path in [r"C:\Windows\SoftwareDistribution", r"C:\Windows\System32\catroot2"]:
            if os.path.exists(path):
                try:
                    os.rename(path, path + ".old")
                except:
                    pass
        
        for svc in services:
            subprocess.run(["net", "start", svc], capture_output=True)
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Windows Update fixed!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def repair_system_files():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[REPAIR SYSTEM FILES]{Colors.END}\n")
    print(f"{Colors.YELLOW}Proses bisa 10-30 menit. JANGAN tutup window!{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    try:
        subprocess.run(["sfc", "/scannow"])
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SFC scan complete!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")