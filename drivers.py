import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime
from colors import Colors


def scan_missing_drivers():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[SCAN MISSING DRIVERS]{Colors.END}\n")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-PnpDevice | Where-Object {$_.Status -ne 'OK'} | Select-Object FriendlyName,Status,Class | Format-Table -AutoSize"], capture_output=True, text=True)
        if result.stdout.strip():
            print(result.stdout)
        else:
            print(f"{Colors.GREEN}✓ Semua driver OK!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def list_all_drivers():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[LIST ALL DRIVERS]{Colors.END}\n")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-WmiObject Win32_PnPSignedDriver | Select-Object DeviceName,Manufacturer,DriverVersion | Format-Table -AutoSize"], capture_output=True, text=True)
        if result.stdout.strip():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = Path.home() / "Desktop" / f"Drivers_{timestamp}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(f"INSTALLED DRIVERS\nGenerated: {datetime.now()}\n\n")
                f.write(result.stdout)
            print(f"{Colors.GREEN}✓ Saved to: {report_file}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def backup_drivers():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[BACKUP DRIVERS]{Colors.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path.home() / "Desktop" / f"DriverBackup_{timestamp}"
    
    print(f"{Colors.CYAN}Backup ke: {backup_dir}{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(["dism", "/online", "/export-driver", f"/destination:{backup_dir}"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Backup complete!{Colors.END}")
            print(f"  Location: {Colors.CYAN}{backup_dir}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def download_snappy_driver():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[SNAPPY DRIVER INSTALLER]{Colors.END}\n")
    print(f"{Colors.YELLOW}SDI = Tool gratis buat install missing drivers.{Colors.END}\n")
    if input(f"{Colors.YELLOW}Buka halaman download? (y/n): {Colors.END}").lower() == 'y':
        webbrowser.open("https://www.snappy-driver-installer.org/")
        print(f"{Colors.GREEN}✓ Browser dibuka{Colors.END}")