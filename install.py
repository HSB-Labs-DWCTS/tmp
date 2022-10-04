# OS Ubuntu 20.04
# Python 3.8.10

#!/usr/bin/python3

import os
import sys
import subprocess

def find_vga():
    print('Find VGA')
    vga = subprocess.Popen("lspci -v -s `lspci | awk '/VGA/{print $1}'`", shell=True)
    savelog = open('install.log', 'w')
    savelog.write(vga)
    savelog.close()
    return vga

def update():
    print('Update and Upgrade')
    os.system('sudo apt update')
    os.system('sudo apt upgrade -y')
    
def check_nvidia():
    if find_vga in 'NVIDIA':
        uninstall_nvidia()
        uninstall_nvidia_cuda()
    else:
        print('Nvidia is not installed')

def uninstall_nvidia():
    print('NVIDIA Uninstall')
    if os.path.exists('/usr/bin/nvidia-smi'):
        print('Nvidia Driver is installed')
        os.system('sudo apt purge nvidia* -y')
        os.system('sudo apt autoremove -y')
        os.system('sudo apt autoclean -y')
    else:
        print('Nvidia Driver is not installed')

def uninstall_nvidia_cuda():    
    print('Uninstall CUDA')
    if os.path.exists('/usr/local/cuda'):
        print('CUDA is installed')
        os.system('sudo rm -fr /usr/local/cuda*')
        os.system('sudo apt --purge remove "cuda*"')
        os.system('sudo apt autoremove --purge "cuda*"')
    else:
        print('CUDA is not installed')

def install():
    print('Install Packages')
    os.system('sudo apt install python3 python3-dev git curl -y')

def install_bootstrap():
    print('Install Bootstrap')
    os.system('curl -sL https://raw.githubusercontent.com/HSB-Labs-DWCTS/the-littlest-jupyterhub-dwcts/main/bootstrap.py | sudo -E python3 - --admin admin')

def change_default_user_interface():
    print('Change default User Interface for users')
    os.system('sudo tljh-config set user_environment.default_app jupyterlab')

def tljs_reload():
    print('Reload')
    os.system('sudo tljh-config reload')

def install_jupyterlab_language_pack():
    print('Install JupyterLab ko-KR Language Pack')
    os.system('sudo -E /opt/tljh/user/bin/conda install -c conda-forge jupyterlab-language-pack-ko-KR -y')

def install_extensions():
    print('Install Extensions')
    os.system('sudo -E /opt/tljh/user/bin/conda install -c conda-forge jupyterlab-git jupyterlab_execute_time -y')
    os.system('sudo -E /opt/tljh/user/bin/pip install jupyterlab-nvdashboard')

def add_path():
    print('Add path')
    os.environ['PATH'] = os.environ['PATH'] + ':/opt/tljh/user/bin'
    subprocess.run("sudo bash -c 'source ~/.bashrc'", shell=True)

def main():
    try:
        update()
        check_nvidia()
        install()
        install_bootstrap()
        change_default_user_interface()
        tljs_reload()
        install_jupyterlab_language_pack()
        install_extensions()
        add_path()
    except Exception as e:
        print(e)
        e_save_log = open('install.log', 'w')
        e_save_log.write(e)
        e_save_log.close()
        sys.exit(1)
