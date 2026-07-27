import sys
import os

sys.path.insert(0, r"d:\enlangg")
from enlang_core.web_server import start_enlang_server

if __name__ == "__main__":
    os.chdir(r"d:\enlangg\aero_portal_3000")
    print("======================================================================")
    print("  STARTING AERO PORTAL ENLANG WEB APPLICATION")
    print("  Folder: d:\\enlangg\\aero_portal_3000")
    print("  Extension Modules: app.enlgf | style.enlgd | server.enlgs | schema.enlgdb")
    print("  Authentication: User 'aero' | Password 'ok@!1234'")
    print("  URL: http://localhost:3000/")
    print("======================================================================")
    start_enlang_server(3000)
