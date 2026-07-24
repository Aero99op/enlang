import sys
import os

sys.path.insert(0, r"d:\enlangg")
from enlang_core.web_server import start_enlang_server

if __name__ == "__main__":
    os.chdir(r"d:\enlangg\aero_app")
    print("Starting AERO Website on http://localhost:4000/ ...")
    start_enlang_server(4000)
