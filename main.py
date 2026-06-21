"""
Office IT Toolkit - Community Edition
All-in-One IT Helper for Office Workers
Made by Dev Fiq (ShafiqGanteng)
"""
import os
import sys
import ctypes
import time

from colors import Colors
from menu import print_banner, print_status, print_menu
from printer import *
from network import *
from system_maintenance import *
from fixes import *
from installer import *
from quick_actions import *
from utility import *
from drivers import *
from security import *
from users import *
from backup import *
from tweaks import *
from remote import *
from config import VERSION, AUTHOR, GITHUB_URL


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)


def show_about():
    """About & credits"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}═══ ABOUT ═══{Colors.END}\n")
    print(f"  {Colors.BOLD}IT Toolkit - Community Edition{Colors.END}")
    print(f"  {Colors.CYAN}Version:{Colors.END} {VERSION}")
    print(f"  {Colors.CYAN}Author :{Colors.END} {AUTHOR}")
    print(f"  {Colors.CYAN}GitHub :{Colors.END} {GITHUB_URL}")
    print(f"  {Colors.CYAN}License:{Colors.END} MIT License")
    print(f"\n{Colors.YELLOW}Description:{Colors.END}")
    print(f"  All-in-one IT helper for office workers.")
    print(f"  Free & open source.")
    print(f"\n{Colors.YELLOW}Features:{Colors.END}")
    print(f"  • Printer Manager (auto-scan network)")
    print(f"  • Network Tools (Wi-Fi, IP, speed test)")
    print(f"  • System Maintenance (cleanup, restart)")
    print(f"  • Driver Manager (scan, backup)")
    print(f"  • Security (Defender, anti-virus)")
    print(f"  • User Account Management")
    print(f"  • Backup & Restore")
    print(f"  • Windows Tweaks")
    print(f"  • Remote Support (RustDesk)")
    print(f"\n{Colors.YELLOW}Contributing:{Colors.END}")
    print(f"  Pull requests welcome! Open issue first.")
    print(f"\n{Colors.GREEN}If this tool helps you, give it a ⭐ on GitHub!{Colors.END}")


def main():
    """Main function"""
    run_as_admin()
    os.system('color')
    os.system('mode con: cols=140 lines=45')
    
    while True:
        os.system('cls')
        print_banner()
        print_status()
        print_menu()
        
        choice = input(f"\n{Colors.BOLD}Pilih menu: {Colors.END}").strip()
        
        actions = {
            # Printer Manager (1-7)
            '1': scan_network_printers,
            '2': add_printer_by_ip,
            '3': list_installed_printers,
            '4': set_default_printer,
            '5': print_test_page,
            '6': remove_printer,
            '7': reset_printer_spooler,
            
            # Network & Wi-Fi (10-14)
            '10': show_wifi_passwords,
            '11': fix_network,
            '12': show_ip_mac,
            '13': test_internet,
            '14': internet_speed_test,
            
            # System Maintenance (20-24)
            '20': clean_temp_files,
            '21': restart_explorer,
            '22': show_system_info,
            '23': unhide_files,
            '24': generate_it_report,
            
            # Common Fixes (30-33)
            '30': fix_audio,
            '31': fix_bluetooth,
            '32': fix_windows_update,
            '33': repair_system_files,
            
            # Driver Manager (40-43)
            '40': scan_missing_drivers,
            '41': list_all_drivers,
            '42': backup_drivers,
            '43': download_snappy_driver,
            
            # Quick Installer (50-52)
            '50': install_common_software,
            '51': install_browsers,
            '52': install_dev_tools,
            
            # Security (60-63)
            '60': windows_defender_scan,
            '61': check_defender_status,
            '62': check_suspicious_startup,
            '63': disable_autorun,
            
            # Backup & Restore (70-71)
            '70': backup_user_profile,
            '71': backup_browser_bookmarks,
            
            # User Account (80-83)
            '80': list_users,
            '81': create_user,
            '82': reset_user_password,
            '83': disable_enable_user,
            
            # Quick Actions (90-93)
            '90': open_device_manager,
            '91': open_disk_cleanup,
            '92': open_services,
            '93': open_control_panel,
            
            # Remote Support (100-101)
            '100': install_rustdesk,
            '101': quick_connect_remote,
            
            # Windows Tweaks (110)
            '110': windows_tweaks_menu,
            
            # Utility (120)
            '120': generate_password,
            
            # About (130)
            '130': show_about,
        }
        
        if choice == '0':
            print(f"\n{Colors.GREEN}Goodbye! Thanks for using IT Toolkit Community! 👋{Colors.END}")
            print(f"{Colors.YELLOW}Star us on GitHub: {GITHUB_URL}{Colors.END}")
            sys.exit(0)
        elif choice in actions:
            actions[choice]()
        else:
            print(f"\n{Colors.RED}✗ Pilihan tidak valid!{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press ENTER...{Colors.END}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}✗ Dibatalkan{Colors.END}")
        sys.exit(0)