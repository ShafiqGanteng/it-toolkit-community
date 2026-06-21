import os
import subprocess
from colors import Colors


def windows_defender_scan():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[WINDOWS DEFENDER SCAN]{Colors.END}\n")
    print(f"  {Colors.CYAN}[1]{Colors.END} Quick Scan (~5 menit)")
    print(f"  {Colors.CYAN}[2]{Colors.END} Full Scan (~1-2 jam)")
    print(f"  {Colors.CYAN}[3]{Colors.END} Custom Scan")
    print(f"  {Colors.RED}[0]{Colors.END} Cancel\n")
    
    choice = input(f"{Colors.YELLOW}Pilih: {Colors.END}").strip()
    try:
        if choice == '1':
            subprocess.run(["powershell", "-Command", "Start-MpScan -ScanType QuickScan"])
            print(f"{Colors.GREEN}✓ Quick scan complete!{Colors.END}")
        elif choice == '2':
            subprocess.run(["powershell", "-Command", "Start-MpScan -ScanType FullScan"])
            print(f"{Colors.GREEN}✓ Full scan complete!{Colors.END}")
        elif choice == '3':
            folder = input(f"{Colors.YELLOW}Path folder: {Colors.END}").strip()
            if os.path.exists(folder):
                subprocess.run(["powershell", "-Command", f"Start-MpScan -ScanType CustomScan -ScanPath '{folder}'"])
                print(f"{Colors.GREEN}✓ Done!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def check_defender_status():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[DEFENDER STATUS]{Colors.END}\n")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-MpComputerStatus | Select AntivirusEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated | Format-List"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def check_suspicious_startup():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[CHECK STARTUP PROGRAMS]{Colors.END}\n")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_StartupCommand | Select Name,Command,Location | Format-Table -AutoSize"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def disable_autorun():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[DISABLE AUTORUN]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    try:
        subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "/v", "NoDriveTypeAutoRun", "/t", "REG_DWORD", "/d", "255", "/f"], capture_output=True)
        print(f"{Colors.GREEN}✓ Autorun disabled!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")