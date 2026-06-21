import os
import subprocess
import shutil
import string
import time
from datetime import datetime
from colors import Colors
from config import SCRIPT_DIR


def clean_temp_files():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[CLEAN TEMP FILES]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    
    temp_dirs = [os.environ.get('TEMP', ''), os.environ.get('TMP', ''), r"C:\Windows\Temp", r"C:\Windows\Prefetch"]
    total_freed = 0
    
    for temp_dir in temp_dirs:
        if not temp_dir or not os.path.exists(temp_dir):
            continue
        print(f"{Colors.CYAN}Cleaning: {temp_dir}{Colors.END}")
        dir_freed = 0
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    os.remove(file_path)
                    dir_freed += size
                except:
                    pass
        freed_mb = dir_freed / (1024 * 1024)
        total_freed += dir_freed
        print(f"  {Colors.GREEN}✓ {freed_mb:.2f} MB{Colors.END}")
    
    print(f"\n{Colors.CYAN}Emptying Recycle Bin...{Colors.END}")
    try:
        subprocess.run(["powershell", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"], check=True, capture_output=True)
        print(f"  {Colors.GREEN}✓ Emptied{Colors.END}")
    except:
        pass
    
    total_mb = total_freed / (1024 * 1024)
    total_gb = total_mb / 1024
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Total cleaned: {total_mb:.2f} MB ({total_gb:.2f} GB){Colors.END}")


def restart_explorer():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[RESTART EXPLORER]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    try:
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
        time.sleep(2)
        subprocess.Popen("explorer.exe")
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Explorer restarted!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def show_system_info():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[SYSTEM INFO]{Colors.END}\n")
    try:
        print(f"{Colors.CYAN}═══ COMPUTER ═══{Colors.END}")
        print(f"  Computer Name  : {Colors.GREEN}{os.environ.get('COMPUTERNAME', 'N/A')}{Colors.END}")
        print(f"  Username       : {Colors.GREEN}{os.environ.get('USERNAME', 'N/A')}{Colors.END}")
        
        print(f"\n{Colors.CYAN}═══ OS ═══{Colors.END}")
        result = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,OSArchitecture | Format-List"], capture_output=True, text=True)
        for line in result.stdout.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                print(f"  {key.strip():<15}: {Colors.GREEN}{value.strip()}{Colors.END}")
        
        print(f"\n{Colors.CYAN}═══ CPU ═══{Colors.END}")
        result = subprocess.run(["powershell", "-Command", "Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors | Format-List"], capture_output=True, text=True)
        for line in result.stdout.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                print(f"  {key.strip():<25}: {Colors.GREEN}{value.strip()}{Colors.END}")
        
        print(f"\n{Colors.CYAN}═══ RAM ═══{Colors.END}")
        result = subprocess.run(["powershell", "-Command", "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"], capture_output=True, text=True)
        print(f"  Total RAM      : {Colors.GREEN}{result.stdout.strip()} GB{Colors.END}")
        
        print(f"\n{Colors.CYAN}═══ DISK ═══{Colors.END}")
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                try:
                    total, used, free = shutil.disk_usage(drive)
                    total_gb = total / (1024**3)
                    used_gb = used / (1024**3)
                    free_gb = free / (1024**3)
                    percent = (used / total) * 100
                    color = Colors.RED if percent > 90 else Colors.YELLOW if percent > 70 else Colors.GREEN
                    print(f"  {drive} {color}{used_gb:.1f}/{total_gb:.1f} GB ({percent:.1f}%) - {free_gb:.1f} GB free{Colors.END}")
                except:
                    pass
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def unhide_files():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[UNHIDE FILES]{Colors.END}\n")
    
    print(f"{Colors.CYAN}Available drives:{Colors.END}")
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            try:
                total, used, free = shutil.disk_usage(drive)
                total_gb = total / (1024**3)
                print(f"  {Colors.GREEN}[{letter}]{Colors.END} {drive} ({total_gb:.1f} GB)")
            except:
                print(f"  {Colors.GREEN}[{letter}]{Colors.END} {drive}")
    
    drive_letter = input(f"\n{Colors.YELLOW}Pilih drive (contoh: E): {Colors.END}").upper().strip()
    target_drive = f"{drive_letter}:\\"
    
    if not os.path.exists(target_drive):
        print(f"{Colors.RED}✗ Drive tidak ditemukan!{Colors.END}")
        return
    
    if input(f"\n{Colors.YELLOW}Unhide files di {target_drive}? (y/n): {Colors.END}").lower() != 'y':
        return
    
    try:
        subprocess.run(f"attrib -h -s -r {target_drive}*.* /s /d", shell=True, capture_output=True)
        
        autorun = os.path.join(target_drive, "autorun.inf")
        if os.path.exists(autorun):
            try:
                subprocess.run(["attrib", "-h", "-s", "-r", autorun], capture_output=True)
                os.remove(autorun)
            except:
                pass
        
        shortcut_count = 0
        try:
            for item in os.listdir(target_drive):
                if item.endswith(".lnk"):
                    try:
                        os.remove(os.path.join(target_drive, item))
                        shortcut_count += 1
                    except:
                        pass
        except:
            pass
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Drive {target_drive} dibersihkan! ({shortcut_count} shortcuts removed){Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def generate_it_report():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[GENERATE IT REPORT]{Colors.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = SCRIPT_DIR / f"IT_Report_{os.environ.get('COMPUTERNAME', 'PC')}_{timestamp}.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"  IT SYSTEM REPORT\n")
            f.write(f"  Generated by: IT Toolkit Community Edition\n")
            f.write(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("[COMPUTER INFO]\n")
            f.write(f"Computer Name : {os.environ.get('COMPUTERNAME', 'N/A')}\n")
            f.write(f"Username      : {os.environ.get('USERNAME', 'N/A')}\n\n")
            
            for section, cmd in [
                ("OS INFO", "Get-CimInstance Win32_OperatingSystem | Select Caption,Version,OSArchitecture | Format-List"),
                ("CPU", "Get-CimInstance Win32_Processor | Select Name,NumberOfCores | Format-List"),
                ("RAM", "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"),
                ("GPU", "Get-CimInstance Win32_VideoController | Select Name | Format-List"),
            ]:
                f.write(f"[{section}]\n")
                result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
                f.write(result.stdout + "\n")
            
            f.write("[DISK INFO]\n")
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    try:
                        total, used, free = shutil.disk_usage(drive)
                        total_gb = total / (1024**3)
                        used_gb = used / (1024**3)
                        free_gb = free / (1024**3)
                        percent = (used / total) * 100
                        f.write(f"  {drive} {used_gb:.1f}/{total_gb:.1f} GB ({percent:.1f}%) - {free_gb:.1f} GB free\n")
                    except:
                        pass
            f.write("\n")
            
            f.write("[NETWORK]\n")
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
            f.write(result.stdout + "\n")
            
            f.write("=" * 70 + "\n")
            f.write("  END OF REPORT\n")
            f.write("=" * 70 + "\n")
        
        print(f"{Colors.GREEN}✓ Report saved to: {report_file}{Colors.END}")
        if input(f"\n{Colors.YELLOW}Buka file? (y/n): {Colors.END}").lower() == 'y':
            os.startfile(report_file)
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")