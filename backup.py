import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from colors import Colors


def backup_user_profile():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[BACKUP USER PROFILE]{Colors.END}\n")
    print(f"{Colors.YELLOW}Backup: Documents, Desktop, Downloads, Pictures{Colors.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path.home() / "Desktop" / f"ProfileBackup_{timestamp}"
    
    folders = {
        "Documents": Path.home() / "Documents",
        "Desktop": Path.home() / "Desktop",
        "Downloads": Path.home() / "Downloads",
        "Pictures": Path.home() / "Pictures",
    }
    
    if input(f"{Colors.YELLOW}Lanjutkan? (y/n): {Colors.END}").lower() != 'y':
        return
    
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        total_size = 0
        for name, source in folders.items():
            if source.exists():
                dest = backup_dir / name
                print(f"{Colors.CYAN}Copying {name}...{Colors.END}")
                try:
                    shutil.copytree(source, dest, dirs_exist_ok=True, ignore_dangling_symlinks=True)
                    folder_size = sum(f.stat().st_size for f in dest.rglob('*') if f.is_file()) / (1024*1024)
                    total_size += folder_size
                    print(f"  {Colors.GREEN}✓ {folder_size:.1f} MB{Colors.END}")
                except Exception as e:
                    print(f"  {Colors.YELLOW}⚠ {e}{Colors.END}")
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Backup complete! Total: {total_size:.1f} MB{Colors.END}")
        print(f"  Location: {Colors.CYAN}{backup_dir}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")


def backup_browser_bookmarks():
    print(f"\n{Colors.CYAN}{Colors.BOLD}[BACKUP BOOKMARKS]{Colors.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path.home() / "Desktop" / f"BookmarksBackup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    browsers = {
        "Chrome": Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Bookmarks",
        "Brave": Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Bookmarks",
        "Edge": Path.home() / "AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks",
    }
    
    found = False
    for browser, path in browsers.items():
        if path.exists():
            try:
                shutil.copy2(path, backup_dir / f"{browser}_Bookmarks")
                print(f"{Colors.GREEN}✓ {browser} backed up{Colors.END}")
                found = True
            except:
                pass
    
    if found:
        print(f"\n{Colors.GREEN}✓ Saved to: {backup_dir}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠ No bookmarks found.{Colors.END}")