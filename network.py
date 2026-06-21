import subprocess
from colors import Colors


def show_wifi_passwords():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[SAVED WI-FI PASSWORDS]{Colors.END}\n")
    try:
        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        profiles = [line.split(":")[1].strip() for line in result.stdout.split("\n") if "All User Profile" in line]
        if not profiles:
            print(f"{Colors.YELLOW}⚠ Tidak ada profile.{Colors.END}")
            return
        print(f"{Colors.BOLD}{'No':<5}{'SSID':<40}{'Password':<30}{Colors.END}")
        print(f"{Colors.CYAN}{'─'*75}{Colors.END}")
        for idx, profile in enumerate(profiles, 1):
            pwd_result = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"], capture_output=True, text=True)
            password = "N/A"
            for line in pwd_result.stdout.split("\n"):
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    break
            color = Colors.GREEN if password != "N/A" else Colors.YELLOW
            print(f"{idx:<5}{profile:<40}{color}{password:<30}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def fix_network():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[FIX NETWORK]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    for label, cmd in [("Flushing DNS",["ipconfig","/flushdns"]),("Releasing IP",["ipconfig","/release"]),("Renewing IP",["ipconfig","/renew"]),("Resetting Winsock",["netsh","winsock","reset"]),("Resetting TCP/IP",["netsh","int","ip","reset"])]:
        print(f"{Colors.CYAN}{label}...{Colors.END}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            print(f"  {Colors.GREEN}✓{Colors.END}" if result.returncode == 0 else f"  {Colors.YELLOW}⚠{Colors.END}")
        except:
            print(f"  {Colors.RED}✗{Colors.END}")
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Done! Restart PC buat efek maksimal.{Colors.END}")


def show_ip_mac():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[IP & MAC ADDRESS]{Colors.END}\n")
    result = subprocess.run(["ipconfig","/all"], capture_output=True, text=True)
    current_adapter = None
    adapter_info = {}
    for line in result.stdout.split("\n"):
        line = line.rstrip()
        if line and not line.startswith(" ") and "adapter" in line.lower():
            current_adapter = line.replace(":","").strip()
            adapter_info[current_adapter] = {}
        elif current_adapter:
            if "Physical Address" in line:
                adapter_info[current_adapter]['MAC'] = line.split(":")[-1].strip()
            elif "IPv4 Address" in line:
                adapter_info[current_adapter]['IPv4'] = line.split(":")[-1].strip().replace("(Preferred)","").strip()
            elif "Default Gateway" in line:
                gw = line.split(":")[-1].strip()
                if gw:
                    adapter_info[current_adapter]['Gateway'] = gw
    for adapter, info in adapter_info.items():
        if info:
            print(f"{Colors.CYAN}═══ {adapter} ═══{Colors.END}")
            for k, v in info.items():
                print(f"  {k:<10}: {Colors.GREEN}{v}{Colors.END}")
            print()


def test_internet():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[TEST INTERNET]{Colors.END}\n")
    for name, target in [("Google DNS","8.8.8.8"),("Cloudflare","1.1.1.1"),("Google.com","google.com"),("YouTube","youtube.com")]:
        print(f"{Colors.CYAN}Pinging {name}...{Colors.END}")
        try:
            result = subprocess.run(["ping","-n","4",target], capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "Average" in line:
                        print(f"  {Colors.GREEN}✓ ({line.split('=')[-1].strip()}){Colors.END}")
                        break
            else:
                print(f"  {Colors.RED}✗ Failed{Colors.END}")
        except:
            print(f"  {Colors.RED}✗ Error{Colors.END}")


def internet_speed_test():
    """Test internet speed pakai speedtest-cli"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[INTERNET SPEED TEST]{Colors.END}\n")
    print(f"{Colors.YELLOW}Testing internet speed... (1-2 menit){Colors.END}\n")
    
    try:
        result = subprocess.run(["python", "-c", "import speedtest"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{Colors.YELLOW}Installing speedtest-cli...{Colors.END}")
            subprocess.run(["pip", "install", "speedtest-cli"], capture_output=True)
    except:
        pass
    
    try:
        print(f"{Colors.CYAN}Connecting to test server...{Colors.END}")
        result = subprocess.run(["python", "-m", "speedtest", "--simple"], capture_output=True, text=True, timeout=120)
        
        if result.stdout.strip():
            print(f"\n{Colors.GREEN}{Colors.BOLD}═══ RESULTS ═══{Colors.END}")
            for line in result.stdout.strip().split("\n"):
                if "Ping" in line:
                    print(f"  {Colors.CYAN}Ping     : {Colors.GREEN}{line.split(':')[1].strip()}{Colors.END}")
                elif "Download" in line:
                    print(f"  {Colors.CYAN}Download : {Colors.GREEN}{line.split(':')[1].strip()}{Colors.END}")
                elif "Upload" in line:
                    print(f"  {Colors.CYAN}Upload   : {Colors.GREEN}{line.split(':')[1].strip()}{Colors.END}")
        else:
            print(f"{Colors.YELLOW}⚠ Speedtest gagal, coba install ulang:{Colors.END}")
            print(f"  pip install --upgrade speedtest-cli")
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}✗ Timeout! Internet lambat banget.{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")