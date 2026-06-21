import subprocess
from colors import Colors


def show_file_extensions():
    print(f"\n{Colors.CYAN}Showing file extensions...{Colors.END}")
    try:
        subprocess.run(["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "/v", "HideFileExt", "/t", "REG_DWORD", "/d", "0", "/f"], capture_output=True)
        print(f"{Colors.GREEN}✓ Done!{Colors.END}")
    except:
        pass


def show_hidden_files():
    print(f"\n{Colors.CYAN}Showing hidden files...{Colors.END}")
    try:
        subprocess.run(["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "/v", "Hidden", "/t", "REG_DWORD", "/d", "1", "/f"], capture_output=True)
        print(f"{Colors.GREEN}✓ Done!{Colors.END}")
    except:
        pass


def disable_bing_search():
    print(f"\n{Colors.CYAN}Disabling Bing search...{Colors.END}")
    try:
        subprocess.run(["reg", "add", r"HKCU\Software\Microsoft\Windows\CurrentVersion\Search", "/v", "BingSearchEnabled", "/t", "REG_DWORD", "/d", "0", "/f"], capture_output=True)
        print(f"{Colors.GREEN}✓ Done!{Colors.END}")
    except:
        pass


def disable_telemetry():
    print(f"\n{Colors.CYAN}Disabling Telemetry...{Colors.END}")
    try:
        subprocess.run(["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "/v", "AllowTelemetry", "/t", "REG_DWORD", "/d", "0", "/f"], capture_output=True)
        print(f"{Colors.GREEN}✓ Done!{Colors.END}")
    except:
        pass


def enable_ultimate_performance():
    print(f"\n{Colors.CYAN}Enabling Ultimate Performance...{Colors.END}")
    try:
        subprocess.run(["powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61"], capture_output=True)
        print(f"{Colors.GREEN}✓ Done! Buka Control Panel → Power Options → pilih Ultimate Performance{Colors.END}")
    except:
        pass


def windows_tweaks_menu():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[WINDOWS TWEAKS]{Colors.END}\n")
    print(f"  {Colors.CYAN}[1]{Colors.END} Show file extensions")
    print(f"  {Colors.CYAN}[2]{Colors.END} Show hidden files")
    print(f"  {Colors.CYAN}[3]{Colors.END} Disable Bing search")
    print(f"  {Colors.CYAN}[4]{Colors.END} Disable Telemetry")
    print(f"  {Colors.CYAN}[5]{Colors.END} Enable Ultimate Performance")
    print(f"  {Colors.GREEN}[A]{Colors.END} Apply Semua")
    print(f"  {Colors.RED}[0]{Colors.END} Cancel\n")
    
    choice = input(f"{Colors.YELLOW}Pilih: {Colors.END}").strip().upper()
    actions = {'1': show_file_extensions, '2': show_hidden_files, '3': disable_bing_search, '4': disable_telemetry, '5': enable_ultimate_performance}
    
    if choice == 'A':
        for action in actions.values():
            action()
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ All tweaks applied!{Colors.END}")
    elif choice in actions:
        actions[choice]()