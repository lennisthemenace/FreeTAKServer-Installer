from jinja2 import Template
import subprocess
import os


def install_pip():
    pip = subprocess.run(["apt", "install", "python3-pip"], capture_output=True)
    return pip.returncode


def install_fts():
    pip = subprocess.run(["python3", "pip", "FreeTAKServer"], capture_output=True)
    return pip.returncode


def link_dir():
    python37_fts_path = "/usr/local/lib/python3.7/dist-packages/FreeTAKServer"
    python38_fts_path = "/usr/local/lib/python3.8/dist-packages/FreeTAKServer"
    if os.path.exists(python37_fts_path):
        os.symlink(python37_fts_path, "./FTS", target_is_directory=True)
    elif os.path.exists(python38_fts_path):
        os.symlink(python38_fts_path, "./FTS", target_is_directory=True)
    else:
        print("Cannot find FreeTAKServer Folder, it may have not been installed")
        return False
    return 0


def install_python_libraries():
    pylibs = subprocess.run(["apt", "install", "python3-dev", "python3-setuptools", "build-essential", "python3-gevent",
                           "python3-lxml", "libcairo2-dev"], capture_output=True)
    return pylibs.returncode


def install_pip_modules():
    pip = subprocess.run(["python3", "pip", "wheel", "pycairo"], capture_output=True)
    return pip.returncode


def install_service():
    system_d_file_template = Template("""[Unit]
    Description=FreeTAK Server Service
    After=network.target
    StartLimitIntervalSec=0
    
    [Service]
    Type=simple
    Restart=always
    RestartSec=1
    ExecStart=/usr/bin/python3 -m FreeTAKServer.controllers.services.FTS -DataPackageIP 0.0.0.0 -AutoStart True
    
    [Install]
    WantedBy=multi-user.target
    """)
    service = system_d_file_template.render()

    with open('/etc/systemd/system/FreeTAKServer.service', 'w') as service_file:
        service_file.write(service)

    subprocess.run(["systemd", "daemon-reload"], capture_output=True)
    subprocess.run(["systemd", "enable", "FreeTAKServer.service"], capture_output=True)
    sysd = subprocess.run(["systemd", "start", "FreeTAKServer.service"], capture_output=True)
    return sysd.returncode


if __name__ == '__main__':
    print("Installing python3 pip")
    if install_pip() != 0:
        print("Something went wrong!")
        exit(1)
    print("------------------------------")
    #print("Installing python libraries")
    #if install_python_libraries() != 0:
    #    print("Something went wrong!")
    #    exit(1)
    print("------------------------------")
    print("Installing pip modules")
    if install_pip_modules() != 0:
        print("Something went wrong!")
        exit(1)
    print("------------------------------")
    print("Installing FreeTAKServer")
    if install_fts() != 0:
        print("Something went wrong!")
        exit(1)
    print("------------------------------")
    print("Installing FreeTAKServer as a system.d service")
    if install_service() != 0:
        print("Something went wrong!")
        exit(1)
    print("------------------------------")
    print("Creating symlinked directory to ./FTS")
    if link_dir() != 0:
        print("Something went wrong!")
    print("------------------------------")
    print("------------------------------")
    print("---------Finished!------------")
    print("------------------------------")
    print("------------------------------")
