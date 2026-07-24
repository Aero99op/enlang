import sys
import os

sys.path.insert(0, r"d:\enlangg")
from enlang_core.web_server import start_enlang_server

if __name__ == "__main__":
    os.chdir(r"d:\enlangg\nexus_app")
    print("Starting NEXUS QUANTUM OS Multipage App on http://localhost:8099/ ...")
    start_enlang_server(8099)
