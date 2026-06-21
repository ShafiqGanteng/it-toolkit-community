import random
import string
from colors import Colors


def generate_password():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[GENERATE STRONG PASSWORD]{Colors.END}\n")
    try:
        length = int(input(f"{Colors.YELLOW}Panjang (default 16): {Colors.END}").strip() or "16")
        count = int(input(f"{Colors.YELLOW}Berapa password (default 5): {Colors.END}").strip() or "5")
    except:
        length = 16
        count = 5
    
    if length < 8:
        length = 8
    if count < 1 or count > 20:
        count = 5
    
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}"
    
    print(f"\n{Colors.CYAN}Generated:{Colors.END}\n")
    for i in range(count):
        password_list = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("!@#$%^&*()_+-=[]{}")
        ]
        for _ in range(length - 4):
            password_list.append(random.choice(chars))
        random.shuffle(password_list)
        password = ''.join(password_list)
        print(f"  {Colors.GREEN}{i+1}.{Colors.END} {Colors.BOLD}{password}{Colors.END}")