import os
import subprocess
import urllib.request
from pathlib import Path
from colors import Colors

RUSTDESK_URL = "https://github.com/rustdesk/rustdesk/releases/download/1.3.2/rustdesk-1.3.2-x86_64.exe"
RUSTDESK_PATH = Path(os.environ['TEMP']) / "rustdesk.exe"


def install_rustdesk():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[INSTALL RUSTDESK]{Colors.END}\n")
    print(f"{Colors.YELLOW}RustDesk = remote desktop gratis open source{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return False
    
    try:
        if not RUSTDESK_PATH.exists():
            print(f"{Colors.CYAN}Downloading RustDesk... (~30 MB){Colors.END}")
            urllib.request.urlretrieve(RUSTDESK_URL, RUSTDESK_PATH)
            print(f"  {Colors.GREEN}✓ Downloaded{Colors.END}")
        
        subprocess.Popen([str(RUSTDESK_PATH)])
        print(f"{Colors.GREEN}✓ RustDesk launched!{Colors.END}")
        print(f"\n{Colors.YELLOW}NEXT STEPS:{Colors.END}")
        print(f"  1. Liat 'ID' (9 digit) di RustDesk")
        print(f"  2. Liat 'Password' (6 digit)")
        print(f"  3. Kasih ID + Password ke yang mau remote")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")
        return False


def quick_connect_remote():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[QUICK CONNECT REMOTE]{Colors.END}\n")
    
    if not RUSTDESK_PATH.exists():
        if not install_rustdesk():
            return
    
    remote_id = input(f"{Colors.YELLOW}Remote ID (9 digit): {Colors.END}").strip()
    if not remote_id:
        return
    
    try:
        subprocess.Popen([str(RUSTDESK_PATH), "--connect", remote_id])
        print(f"{Colors.GREEN}✓ Connecting to {remote_id}...{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")