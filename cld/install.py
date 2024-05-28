import subprocess
import sys 
import os
import ctypes
import time


sys_info = sys.platform
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def run_exe_with_admin_permission(exe_path):
    if is_admin():
        try:
            result = os.system(exe_path)
            if result != 0:
                raise PermissionError(RED+f"Failed to run {exe_path}. Exit code: {result}"+RESET)
        except Exception as e:
            print(RED+f"Error running {exe_path}: {e}")
            raise PermissionError(f"Failed to run {exe_path}: {e}"+RESET)
    else:
        try:
            result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            if result <= 32:
                raise PermissionError(RED+f"Failed to install graphviz! Exit code: {result}"+RESET)
        except:
            raise PermissionError(YELLOW+"Failed to install graphviz! Please ensure you have admin privileges before retrying."+RESET)
        
def is_graphviz_installed():
    try:
        subprocess.run(["dot", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_packages():
    if sys_info == "win32":
        print(YELLOW+"Detected OS Windows\nInstalling Graphviz2.6..."+RESET)
        if not is_graphviz_installed():

            try:
                run_exe_with_admin_permission("stable_windows_10_cmake_Release_x64_graphviz-install-2.46.0-win64.exe")
            except PermissionError as e:
                sys.exit(e)

            while not is_graphviz_installed():
                print(YELLOW+"Waiting for Graphviz installation to complete. If installation is complete and you're still seeing this message, that means you need to add graphviz to PATH."+RESET)
                time.sleep(15)

            print("Graphviz installation completed successfully.")
        else:
            print("Found existing graphviz installation. Continuing to pygraphviz installation.")
        print("Installing pygraphviz...")
        try:
            subprocess.run([
                'python', '-m', 'pip', 'install', '--use-pep517',
                '--config-setting=--global-option=build_ext',
                '--config-setting=--global-option=-IC:\\Program Files\\Graphviz\\include',
                '--config-setting=--global-option=-LC:\\Program Files\\Graphviz\\lib',
                'pygraphviz'
            ])

        except KeyboardInterrupt:
            sys.exit(YELLOW+"Detected keyboard interrupt.\nStopping..."+RESET)
        except Exception as e:
            sys.exit(f"Something unexpected occured. Either Graphviz was not installed correctly, or there is a version conflict. Just give up.\nException: {e}")
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
            

    elif sys_info == "linux":
        print(YELLOW+"Detected OS linux\nInstalling Graphviz..."+RESET)
        try:
            subprocess.run(["sudo", "apt-get", "install", "graphviz", "graphviz-dev"])
        except PermissionError:
            print(YELLOW+"Admin privileges not found. Trying to run without sudo."+RESET)
            subprocess.run(["apt-get", "install", "graphviz", "graphviz-dev"])
        except Exception as e:
            sys.exit(RED+"Bruh idk whats wrong... Maybe you don't have python. Or gcc idk."+RESET)
        print("Installing pygraphviz...")
        subprocess.run(["pip", "install", "pygraphviz"])
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
        print("Installation completed successfully!")

    elif sys_info == "darwin":
        print(YELLOW+"Detected OS darwin\nInstalling Graphviz..."+RESET)
        try:
            subprocess.run(["brew", "install", "graphviz"])
        except Exception as e:
            sys.exit(RED+f"Graphviz installation failed! Error: {e}"+RESET)
        print("Graphviz installed successfully!")
        print("Installing pygraphviz...")
        try:
            subprocess.run([
                'pip', 'install', '--use-pep517',
                '--config-setting=--global-option=build_ext',
                f'--config-setting=--build-option=-I$(brew --prefix graphviz)/include/',
                f'--config-setting=--build-option=-L$(brew --prefix graphviz)/lib/',
                'pygraphviz'
            ])
        except:
            sys.exit(BLUE+"Please report your exact error to Aritra (aritram21@vt.edu)"+RESET)
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
    else:
        print("OS is unsupported. Os has to be either Windows, Linux, or MacOS.")

if __name__ == "__main__":
    install_packages()