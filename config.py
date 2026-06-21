"""
Office IT Toolkit - Community Edition
Configuration File
"""
import tempfile
from pathlib import Path
import sys

# ==============================================
# APP CONFIGURATION
# ==============================================

VERSION = "3.0 Community Edition"
AUTHOR = "Dev Fiq (ShafiqGanteng)"
GITHUB_URL = "https://github.com/ShafiqGanteng/it-toolkit-community"

# ==============================================
# PATHS
# ==============================================

def get_script_dir():
    """Get folder tempat script ini berada"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

SCRIPT_DIR = get_script_dir()
TEMP_DIR = Path(tempfile.gettempdir()) / "ITToolkitCommunity"