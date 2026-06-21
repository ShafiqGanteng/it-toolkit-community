import subprocess
from colors import Colors


def install_common_software():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[INSTALL COMMON SOFTWARE]{Colors.END}\n")
    software = [
        ("Google Chrome", "Google.Chrome"),
        ("Brave Browser", "Brave.Brave"),
        ("7-Zip", "7zip.7zip"),
        ("VLC Media Player", "VideoLAN.VLC"),
        ("Adobe Acrobat Reader", "Adobe.Acrobat.Reader.64-bit"),
        ("Notepad++", "Notepad++.Notepad++"),
        ("Microsoft PowerToys", "Microsoft.PowerToys"),
        ("WhatsApp Desktop", "9NKSQGP7F2NH"),
        ("Telegram Desktop", "Telegram.TelegramDesktop"),
        ("Zoom", "Zoom.Zoom"),
    ]
    for idx, (name, _) in enumerate(software, 1):
        print(f"  {Colors.CYAN}[{idx}]{Colors.END} {name}")
    print(f"  {Colors.GREEN}[A]{Colors.END} Install Semua")
    print(f"  {Colors.RED}[0]{Colors.END} Cancel")
    
    choice = input(f"\n{Colors.YELLOW}Pilihan (contoh: 1,3,5 atau A): {Colors.END}").strip().upper()
    if choice == '0':
        return
    
    to_install = software if choice == 'A' else [software[i-1] for i in [int(x.strip()) for x in choice.split(",")] if 1 <= i <= len(software)]
    
    for name, pkg_id in to_install:
        print(f"{Colors.CYAN}Installing {name}...{Colors.END}")
        try:
            subprocess.run(["winget", "install", pkg_id, "-e", "--accept-source-agreements", "--accept-package-agreements"], capture_output=True, timeout=300)
            print(f"  {Colors.GREEN}✓ Done{Colors.END}")
        except:
            print(f"  {Colors.RED}✗ Error{Colors.END}")


def install_browsers():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[INSTALL BROWSERS]{Colors.END}\n")
    browsers = [
        ("Google Chrome", "Google.Chrome"),
        ("Brave Browser", "Brave.Brave"),
        ("Mozilla Firefox", "Mozilla.Firefox"),
        ("Microsoft Edge", "Microsoft.Edge"),
        ("Opera", "Opera.Opera"),
    ]
    for idx, (name, _) in enumerate(browsers, 1):
        print(f"  {Colors.CYAN}[{idx}]{Colors.END} {name}")
    print(f"  {Colors.RED}[0]{Colors.END} Cancel")
    try:
        choice = int(input(f"\n{Colors.YELLOW}Pilih: {Colors.END}"))
        if 1 <= choice <= len(browsers):
            name, pkg_id = browsers[choice - 1]
            print(f"\n{Colors.CYAN}Installing {name}...{Colors.END}")
            subprocess.run(["winget", "install", pkg_id, "-e", "--accept-source-agreements", "--accept-package-agreements"], timeout=300)
            print(f"\n{Colors.GREEN}✓ Done!{Colors.END}")
    except:
        print(f"{Colors.RED}✗ Invalid!{Colors.END}")


def install_dev_tools():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[INSTALL DEV TOOLS]{Colors.END}\n")
    tools = [
        ("Visual Studio Code", "Microsoft.VisualStudioCode"),
        ("Git", "Git.Git"),
        ("Python 3.12", "Python.Python.3.12"),
        ("Node.js LTS", "OpenJS.NodeJS.LTS"),
        ("Windows Terminal", "Microsoft.WindowsTerminal"),
        ("Postman", "Postman.Postman"),
    ]
    for idx, (name, _) in enumerate(tools, 1):
        print(f"  {Colors.CYAN}[{idx}]{Colors.END} {name}")
    print(f"  {Colors.GREEN}[A]{Colors.END} Install Semua")
    print(f"  {Colors.RED}[0]{Colors.END} Cancel")
    
    choice = input(f"\n{Colors.YELLOW}Pilihan: {Colors.END}").strip().upper()
    if choice == '0':
        return
    
    to_install = tools if choice == 'A' else [tools[i-1] for i in [int(x.strip()) for x in choice.split(",")] if 1 <= i <= len(tools)]
    
    for name, pkg_id in to_install:
        print(f"{Colors.CYAN}Installing {name}...{Colors.END}")
        try:
            subprocess.run(["winget", "install", pkg_id, "-e", "--accept-source-agreements", "--accept-package-agreements"], capture_output=True, timeout=300)
            print(f"  {Colors.GREEN}✓ Done{Colors.END}")
        except:
            print(f"  {Colors.RED}✗ Error{Colors.END}")