import subprocess
from colors import Colors


def list_users():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[LIST USERS]{Colors.END}\n")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-LocalUser | Select Name,Enabled,Description | Format-Table -AutoSize"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def create_user():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[CREATE USER]{Colors.END}\n")
    username = input(f"{Colors.YELLOW}Username: {Colors.END}").strip()
    if not username:
        return
    password = input(f"{Colors.YELLOW}Password: {Colors.END}").strip()
    is_admin = input(f"{Colors.YELLOW}Jadiin Administrator? (y/n): {Colors.END}").lower() == 'y'
    
    try:
        if password:
            cmd = f"$pw = ConvertTo-SecureString '{password}' -AsPlainText -Force; New-LocalUser -Name '{username}' -Password $pw"
        else:
            cmd = f"New-LocalUser -Name '{username}' -NoPassword"
        subprocess.run(["powershell", "-Command", cmd], capture_output=True)
        subprocess.run(["powershell", "-Command", f"Add-LocalGroupMember -Group 'Users' -Member '{username}'"], capture_output=True)
        if is_admin:
            subprocess.run(["powershell", "-Command", f"Add-LocalGroupMember -Group 'Administrators' -Member '{username}'"], capture_output=True)
        print(f"\n{Colors.GREEN}✓ User '{username}' created!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def reset_user_password():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[RESET PASSWORD]{Colors.END}\n")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-LocalUser | Select -ExpandProperty Name"], capture_output=True, text=True)
        users = [u.strip() for u in result.stdout.strip().split("\n") if u.strip()]
        if not users:
            return
        for idx, user in enumerate(users, 1):
            print(f"  {Colors.CYAN}[{idx}]{Colors.END} {user}")
        choice = int(input(f"\n{Colors.YELLOW}Pilih: {Colors.END}"))
        if 1 <= choice <= len(users):
            new_pass = input(f"{Colors.YELLOW}Password baru: {Colors.END}").strip()
            cmd = f"$pw = ConvertTo-SecureString '{new_pass}' -AsPlainText -Force; Set-LocalUser -Name '{users[choice-1]}' -Password $pw"
            subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            print(f"\n{Colors.GREEN}✓ Password reset!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def disable_enable_user():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[ENABLE/DISABLE USER]{Colors.END}\n")
    try:
        result = subprocess.run(["powershell", "-Command", "Get-LocalUser | Select Name,Enabled | Format-Table"], capture_output=True, text=True)
        print(result.stdout)
        username = input(f"{Colors.YELLOW}Username: {Colors.END}").strip()
        action = input(f"{Colors.YELLOW}Enable/Disable? (e/d): {Colors.END}").lower()
        if action == 'e':
            subprocess.run(["powershell", "-Command", f"Enable-LocalUser -Name '{username}'"], capture_output=True)
            print(f"\n{Colors.GREEN}✓ Enabled!{Colors.END}")
        elif action == 'd':
            subprocess.run(["powershell", "-Command", f"Disable-LocalUser -Name '{username}'"], capture_output=True)
            print(f"\n{Colors.GREEN}✓ Disabled!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")