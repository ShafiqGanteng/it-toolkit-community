import os
import re
import subprocess
import socket
import ipaddress
import urllib.request
from colors import Colors


def get_local_ip_range():
    """Detect IP range dari laptop"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        ip_parts = local_ip.split(".")
        network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        return local_ip, network
    except:
        return None, None


def check_printer_port(ip, port=9100, timeout=0.5):
    """Cek printer port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False


def get_printer_name(ip, timeout=2):
    """Get printer name pakai 3 method"""
    try:
        url = f"http://{ip}/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=timeout)
        html = response.read(3000).decode('utf-8', errors='ignore')
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            title = re.sub(r'\s+', ' ', title_match.group(1).strip())
            if title and len(title) > 2 and len(title) < 80:
                return title[:50]
    except:
        pass
    
    try:
        import ssl
        url = f"https://{ip}/"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        html = response.read(3000).decode('utf-8', errors='ignore')
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            title = re.sub(r'\s+', ' ', title_match.group(1).strip())
            if title and len(title) > 2 and len(title) < 80:
                return title[:50]
    except:
        pass
    
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        if hostname:
            name = hostname.split('.')[0]
            if name and len(name) > 2:
                return name
    except:
        pass
    
    return "Unknown Printer"


def scan_network_printers():
    """Auto-scan printer di network dengan detect nama"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[AUTO-SCAN PRINTER]{Colors.END}\n")
    
    local_ip, network = get_local_ip_range()
    if not local_ip:
        print(f"{Colors.RED}✗ Gak bisa detect network!{Colors.END}")
        return
    
    print(f"{Colors.CYAN}Your IP: {Colors.GREEN}{local_ip}{Colors.END}")
    print(f"{Colors.CYAN}Range  : {Colors.GREEN}{network}{Colors.END}")
    print(f"{Colors.YELLOW}Scanning... (2-3 menit){Colors.END}\n")
    
    try:
        net = ipaddress.ip_network(network, strict=False)
        all_ips = [str(ip) for ip in net.hosts()]
    except:
        return
    
    found = []
    total = len(all_ips)
    
    print(f"{Colors.CYAN}Phase 1: Scanning ports...{Colors.END}")
    for idx, ip in enumerate(all_ips, 1):
        if idx % 25 == 0 or idx == total:
            print(f"\r  {Colors.CYAN}Progress: {idx}/{total} ({(idx/total)*100:.0f}%){Colors.END}", end="")
        if ip == local_ip:
            continue
        for port, proto in [(9100, 'RAW'), (631, 'IPP'), (515, 'LPR')]:
            if check_printer_port(ip, port, 0.3):
                found.append({'ip': ip, 'port': port, 'protocol': proto, 'name': 'Detecting...'})
                break
    
    if not found:
        print(f"\n\n{Colors.YELLOW}⚠ Tidak ada printer ditemukan.{Colors.END}")
        return
    
    print(f"\n\n{Colors.CYAN}Phase 2: Getting printer names...{Colors.END}")
    for idx, printer in enumerate(found, 1):
        print(f"\r  {Colors.CYAN}Resolving {idx}/{len(found)}: {printer['ip']}{Colors.END}", end="")
        printer['name'] = get_printer_name(printer['ip'], timeout=2)
    
    print(f"\n\n{Colors.GREEN}{Colors.BOLD}═══ SCAN COMPLETE ═══{Colors.END}\n")
    print(f"{Colors.GREEN}✓ Ditemukan {len(found)} printer:{Colors.END}\n")
    print(f"{Colors.BOLD}{'No':<5}{'IP Address':<18}{'Port':<8}{'Protocol':<10}{'Printer Name':<45}{Colors.END}")
    print(f"{Colors.CYAN}{'─'*85}{Colors.END}")
    
    for idx, p in enumerate(found, 1):
        name_color = Colors.GREEN if p['name'] != "Unknown Printer" else Colors.YELLOW
        print(f"{Colors.GREEN}{idx:<5}{Colors.END}{p['ip']:<18}{p['port']:<8}{p['protocol']:<10}{name_color}{p['name'][:43]:<45}{Colors.END}")
    
    add_now = input(f"\n{Colors.YELLOW}Add salah satu? (y/n): {Colors.END}").lower()
    if add_now == 'y':
        try:
            num = int(input(f"{Colors.YELLOW}Pilih nomor: {Colors.END}"))
            if 1 <= num <= len(found):
                selected = found[num - 1]
                add_printer_by_ip_with_name(selected['ip'], selected['name'])
        except:
            print(f"{Colors.RED}✗ Input tidak valid!{Colors.END}")


def add_printer_by_ip_with_name(ip, default_name="Network Printer"):
    """Add printer by IP dengan nama default dari hasil scan"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[ADD PRINTER]{Colors.END}\n")
    print(f"{Colors.CYAN}IP Address    : {Colors.GREEN}{ip}{Colors.END}")
    print(f"{Colors.CYAN}Detected Name : {Colors.GREEN}{default_name}{Colors.END}\n")
    
    suggested_name = default_name if default_name != "Unknown Printer" else f"Network Printer ({ip})"
    printer_name = input(f"{Colors.YELLOW}Nama printer (default: {suggested_name}): {Colors.END}").strip()
    if not printer_name:
        printer_name = suggested_name
    
    try:
        port_name = f"IP_{ip}"
        subprocess.run(["powershell", "-Command", f"Add-PrinterPort -Name '{port_name}' -PrinterHostAddress '{ip}' -ErrorAction SilentlyContinue"], capture_output=True)
        subprocess.run(["powershell", "-Command", "Add-PrinterDriver -Name 'Generic / Text Only' -ErrorAction SilentlyContinue"], capture_output=True)
        result = subprocess.run(["powershell", "-Command", f"Add-Printer -Name '{printer_name}' -DriverName 'Generic / Text Only' -PortName '{port_name}' -ErrorAction Stop"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Printer '{printer_name}' berhasil di-add!{Colors.END}")
        else:
            print(f"{Colors.RED}✗ Gagal: {result.stderr[:200] if result.stderr else 'Unknown error'}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def add_printer_by_ip(ip=None):
    """Add printer by IP manual"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[ADD PRINTER BY IP]{Colors.END}\n")
    
    if not ip:
        ip = input(f"{Colors.YELLOW}IP printer: {Colors.END}").strip()
    
    try:
        ipaddress.ip_address(ip)
    except:
        print(f"{Colors.RED}✗ IP tidak valid!{Colors.END}")
        return
    
    print(f"{Colors.CYAN}Detecting printer name...{Colors.END}")
    detected_name = get_printer_name(ip, timeout=3)
    
    if detected_name != "Unknown Printer":
        print(f"{Colors.GREEN}✓ Detected: {detected_name}{Colors.END}")
        suggested_name = detected_name
    else:
        suggested_name = f"Network Printer ({ip})"
    
    printer_name = input(f"\n{Colors.YELLOW}Nama (default: {suggested_name}): {Colors.END}").strip() or suggested_name
    
    try:
        port_name = f"IP_{ip}"
        subprocess.run(["powershell", "-Command", f"Add-PrinterPort -Name '{port_name}' -PrinterHostAddress '{ip}' -ErrorAction SilentlyContinue"], capture_output=True)
        subprocess.run(["powershell", "-Command", "Add-PrinterDriver -Name 'Generic / Text Only' -ErrorAction SilentlyContinue"], capture_output=True)
        result = subprocess.run(["powershell", "-Command", f"Add-Printer -Name '{printer_name}' -DriverName 'Generic / Text Only' -PortName '{port_name}' -ErrorAction Stop"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Printer '{printer_name}' berhasil di-add!{Colors.END}")
        else:
            print(f"{Colors.RED}✗ Gagal{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def list_installed_printers():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[INSTALLED PRINTERS]{Colors.END}\n")
    result = subprocess.run(["powershell", "-Command", "Get-Printer | Select Name,PortName,DriverName,PrinterStatus | Format-Table -AutoSize"], capture_output=True, text=True)
    print(result.stdout if result.stdout.strip() else f"{Colors.YELLOW}⚠ Tidak ada printer.{Colors.END}")


def set_default_printer():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[SET DEFAULT PRINTER]{Colors.END}\n")
    result = subprocess.run(["powershell", "-Command", "Get-Printer | Select -ExpandProperty Name"], capture_output=True, text=True)
    printers = [p.strip() for p in result.stdout.strip().split("\n") if p.strip()]
    if not printers:
        print(f"{Colors.YELLOW}⚠ Tidak ada printer.{Colors.END}")
        return
    for i, p in enumerate(printers, 1):
        print(f"  {Colors.CYAN}[{i}]{Colors.END} {p}")
    try:
        c = int(input(f"\n{Colors.YELLOW}Pilih: {Colors.END}"))
        if 1 <= c <= len(printers):
            subprocess.run(["powershell", "-Command", f"(New-Object -ComObject WScript.Network).SetDefaultPrinter('{printers[c-1]}')"], capture_output=True)
            print(f"\n{Colors.GREEN}✓ Default: {printers[c-1]}{Colors.END}")
    except:
        print(f"{Colors.RED}✗ Invalid!{Colors.END}")


def print_test_page():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[PRINT TEST PAGE]{Colors.END}\n")
    result = subprocess.run(["powershell", "-Command", "Get-Printer | Select -ExpandProperty Name"], capture_output=True, text=True)
    printers = [p.strip() for p in result.stdout.strip().split("\n") if p.strip()]
    if not printers:
        return
    for i, p in enumerate(printers, 1):
        print(f"  {Colors.CYAN}[{i}]{Colors.END} {p}")
    try:
        c = int(input(f"\n{Colors.YELLOW}Pilih: {Colors.END}"))
        if 1 <= c <= len(printers):
            subprocess.run(["powershell", "-Command", f"$p = Get-WmiObject -Query \"SELECT * FROM Win32_Printer WHERE Name='{printers[c-1]}'\"; $p.PrintTestPage()"], capture_output=True)
            print(f"{Colors.GREEN}✓ Test page sent!{Colors.END}")
    except:
        print(f"{Colors.RED}✗ Invalid!{Colors.END}")


def remove_printer():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[REMOVE PRINTER]{Colors.END}\n")
    result = subprocess.run(["powershell", "-Command", "Get-Printer | Select -ExpandProperty Name"], capture_output=True, text=True)
    printers = [p.strip() for p in result.stdout.strip().split("\n") if p.strip()]
    if not printers:
        return
    for i, p in enumerate(printers, 1):
        print(f"  {Colors.CYAN}[{i}]{Colors.END} {p}")
    try:
        c = int(input(f"\n{Colors.YELLOW}Pilih: {Colors.END}"))
        if 1 <= c <= len(printers):
            if input(f"\n{Colors.RED}Hapus '{printers[c-1]}'? (y/n): {Colors.END}").lower() == 'y':
                subprocess.run(["powershell", "-Command", f"Remove-Printer -Name '{printers[c-1]}'"], capture_output=True)
                print(f"{Colors.GREEN}✓ Dihapus!{Colors.END}")
    except:
        print(f"{Colors.RED}✗ Invalid!{Colors.END}")


def reset_printer_spooler():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[RESET SPOOLER]{Colors.END}\n")
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    try:
        subprocess.run(["net", "stop", "spooler"], check=True, capture_output=True)
        spool_dir = r"C:\Windows\System32\spool\PRINTERS"
        cleared = 0
        if os.path.exists(spool_dir):
            for f in os.listdir(spool_dir):
                try:
                    os.remove(os.path.join(spool_dir, f))
                    cleared += 1
                except:
                    pass
        subprocess.run(["net", "start", "spooler"], check=True, capture_output=True)
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Spooler reset! ({cleared} files cleared){Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")