import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "avariados"))

from avariados.wsgi import application