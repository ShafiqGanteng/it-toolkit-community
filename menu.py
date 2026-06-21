import os
import shutil
from colors import Colors
from config import VERSION, AUTHOR


def get_terminal_width():
    """Get terminal width"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 140


def print_banner():
    """Print banner yang ter-CENTER di tengah layar"""
    width = get_terminal_width()
    
    banner_lines = [
        "╔══════════════════════════════════════════════════════════╗",
        "║                                                          ║",
        "║          🛠️    IT TOOLKIT - COMMUNITY    🛠️              ║",
        "║                                                          ║",
        "║         All-in-One IT Helper for Office Workers          ║",
        "║                                                          ║",
        "║                    Made By Dev Fiq                       ║",
        "║                Open Source - MIT License                 ║",
        "║                                                          ║",
        "╚══════════════════════════════════════════════════════════╝",
    ]
    
    print()
    for line in banner_lines:
        padding = (width - len(line)) // 2
        spaces = " " * max(0, padding)
        print(f"{spaces}{Colors.CYAN}{Colors.BOLD}{line}{Colors.END}")
    print()


def print_status():
    """Print status info"""
    width = get_terminal_width()
    
    status = f"v{VERSION} | github.com/ShafiqGanteng/it-toolkit-community"
    padding = (width - len(status)) // 2
    spaces = " " * max(0, padding)
    
    print(f"{spaces}{Colors.YELLOW}{status}{Colors.END}")
    print()


def print_menu():
    """Print main menu - layout multi kolom"""
    menu = f"""
{Colors.BOLD}════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{Colors.END}
{Colors.HEADER}{Colors.BOLD}  🖨️  PRINTER MANAGER                      🌐 NETWORK & WI-FI                       🛡️  SYSTEM MAINTENANCE{Colors.END}
{Colors.CYAN}  [1]{Colors.END}  Auto-Scan Printer (Network)      {Colors.CYAN}[10]{Colors.END} Show Wi-Fi Passwords           {Colors.CYAN}[20]{Colors.END} Clean Temp Files
{Colors.CYAN}  [2]{Colors.END}  Add Printer by IP                {Colors.CYAN}[11]{Colors.END} Fix Network (DNS/IP Reset)     {Colors.CYAN}[21]{Colors.END} Restart Windows Explorer
{Colors.CYAN}  [3]{Colors.END}  List Installed Printers          {Colors.CYAN}[12]{Colors.END} Show IP & MAC Address          {Colors.CYAN}[22]{Colors.END} System Info Lengkap
{Colors.CYAN}  [4]{Colors.END}  Set Default Printer              {Colors.CYAN}[13]{Colors.END} Test Internet (Ping)           {Colors.CYAN}[23]{Colors.END} Unhide Files (Anti Virus)
{Colors.CYAN}  [5]{Colors.END}  Print Test Page                  {Colors.CYAN}[14]{Colors.END} Internet Speed Test ⚡         {Colors.CYAN}[24]{Colors.END} Generate IT Report
{Colors.CYAN}  [6]{Colors.END}  Remove Printer
{Colors.CYAN}  [7]{Colors.END}  Reset Printer Spooler            {Colors.HEADER}{Colors.BOLD}🔧 COMMON FIXES{Colors.END}                      {Colors.HEADER}{Colors.BOLD}💾 DRIVER MANAGER{Colors.END}
                                            {Colors.CYAN}[30]{Colors.END} Fix Audio (No Sound)           {Colors.CYAN}[40]{Colors.END} Scan Missing Drivers
{Colors.HEADER}{Colors.BOLD}  🚀 QUICK INSTALLER                       {Colors.CYAN}[31]{Colors.END} Fix Bluetooth                  {Colors.CYAN}[41]{Colors.END} List All Drivers
{Colors.CYAN}  [50]{Colors.END} Install Common Software          {Colors.CYAN}[32]{Colors.END} Fix Windows Update Stuck       {Colors.CYAN}[42]{Colors.END} Backup All Drivers
{Colors.CYAN}  [51]{Colors.END} Install Web Browsers             {Colors.CYAN}[33]{Colors.END} Repair System Files (SFC)      {Colors.CYAN}[43]{Colors.END} Download SDI (3rd Party)
{Colors.CYAN}  [52]{Colors.END} Install Dev Tools

{Colors.HEADER}{Colors.BOLD}  🛡️  SECURITY                             💼 BACKUP & RESTORE                  👥 USER ACCOUNT{Colors.END}
{Colors.CYAN}  [60]{Colors.END} Windows Defender Scan            {Colors.CYAN}[70]{Colors.END} Backup User Profile            {Colors.CYAN}[80]{Colors.END} List Users
{Colors.CYAN}  [61]{Colors.END} Check Defender Status            {Colors.CYAN}[71]{Colors.END} Backup Browser Bookmarks       {Colors.CYAN}[81]{Colors.END} Create New User
{Colors.CYAN}  [62]{Colors.END} Check Suspicious Startup                                                  {Colors.CYAN}[82]{Colors.END} Reset User Password
{Colors.CYAN}  [63]{Colors.END} Disable Autorun (Anti USB Virus)                                          {Colors.CYAN}[83]{Colors.END} Enable/Disable User

{Colors.HEADER}{Colors.BOLD}  ⚙️  QUICK ACTIONS                         🖥️  REMOTE SUPPORT                    ⚙️  WINDOWS TWEAKS{Colors.END}
{Colors.CYAN}  [90]{Colors.END} Open Device Manager              {Colors.CYAN}[100]{Colors.END} Install RustDesk              {Colors.CYAN}[110]{Colors.END} Windows Tweaks Menu
{Colors.CYAN}  [91]{Colors.END} Open Disk Cleanup                {Colors.CYAN}[101]{Colors.END} Quick Connect Remote
{Colors.CYAN}  [92]{Colors.END} Open Services
{Colors.CYAN}  [93]{Colors.END} Open Control Panel               {Colors.HEADER}{Colors.BOLD}🔧 UTILITY{Colors.END}                          {Colors.HEADER}{Colors.BOLD}ℹ️  ABOUT{Colors.END}
                                            {Colors.CYAN}[120]{Colors.END} Generate Strong Password      {Colors.CYAN}[130]{Colors.END} About & Credits
                                                                                          {Colors.RED}[0]{Colors.END}   Exit
{Colors.BOLD}════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════{Colors.END}
"""
    print(menu)