import subprocess
from colors import Colors


def open_device_manager():
    print(f"\n{Colors.CYAN}Opening Device Manager...{Colors.END}")
    subprocess.Popen(["devmgmt.msc"], shell=True)
    print(f"{Colors.GREEN}✓ Opened{Colors.END}")


def open_disk_cleanup():
    print(f"\n{Colors.CYAN}Opening Disk Cleanup...{Colors.END}")
    subprocess.Popen(["cleanmgr.exe"])
    print(f"{Colors.GREEN}✓ Opened{Colors.END}")


def open_services():
    print(f"\n{Colors.CYAN}Opening Services...{Colors.END}")
    subprocess.Popen(["services.msc"], shell=True)
    print(f"{Colors.GREEN}✓ Opened{Colors.END}")


def open_control_panel():
    print(f"\n{Colors.CYAN}Opening Control Panel...{Colors.END}")
    subprocess.Popen(["control.exe"])
    print(f"{Colors.GREEN}✓ Opened{Colors.END}")