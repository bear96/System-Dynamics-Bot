import subprocess
import sys
import os

sys_info = sys.platform
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def uninstall_packages():
    if sys_info == "win32":
        try:
            subprocess.run(["pip", "uninstall", "-y", "pygraphviz"])
            try:
                subprocess.run(["pip", "uninstall", "-y", "graphviz"])
                print(RED+"If you see a warning that graphviz was not installed despite it being installed, you will need to uninstall graphviz manually from control panel."+RESET)
            except Exception as e:
                print(f"{e}\nContinuing to uninstall other modules.")
            print("Uninstalled pygraphviz and graphviz.")
        except Exception as e:
            print(f"Error uninstalling pygraphviz and graphviz: {e}")

        subprocess.run(["pip", "uninstall", "-r", "requirements.txt", "-y"])
        print("Uninstalled packages successfully!")
    
    elif sys_info == "linux":
        try:
            subprocess.run(["pip", "uninstall", "-y", "pygraphviz"])
            subprocess.run(["sudo", "apt-get", "remove", "--purge", "graphviz"])
            print("Uninstalled pygraphviz and graphviz.")
        except Exception as e:
            print(f"Error uninstalling pygraphviz and graphviz: {e}")
        subprocess.run(["pip", "uninstall", "-r", "requirements.txt", "-y"])
        print("Uninstalled packages successfully!")
    
    elif sys_info == "darwin":
        try:
            subprocess.run(["pip", "uninstall", "-y", "pygraphviz"])
            subprocess.run(["brew", "uninstall", "graphviz"])
            print("Uninstalled pygraphviz and graphviz.")
        except Exception as e:
            print(f"Error uninstalling pygraphviz and graphviz: {e}")
        subprocess.run(["pip", "uninstall", "-r", "requirements.txt", "-y"])
        print("Uninstalled packages successfully!")
    else:
        print("Unsupported OS")

if __name__ == "__main__":
    uninstall_packages()
