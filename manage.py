import os
import sys
from pathlib import Path

# adiciona a pasta gomesmoveis no path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "gomesmoveis"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gomesmoveis.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)