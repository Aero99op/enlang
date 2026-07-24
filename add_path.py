import os
import winreg

def add_to_path(folder):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_ALL_ACCESS)
        try:
            path_val, _ = winreg.QueryValueEx(key, 'Path')
        except FileNotFoundError:
            path_val = ''

        folders = path_val.split(';') if path_val else []
        if folder not in folders and folder.lower() not in [f.lower() for f in folders]:
            new_path = path_val + (';' if path_val and not path_val.endswith(';') else '') + folder
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"Successfully added '{folder}' to User PATH!")
        else:
            print(f"'{folder}' is already in User PATH.")
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error setting PATH: {e}")

if __name__ == '__main__':
    add_to_path(r'd:\enlangg')
