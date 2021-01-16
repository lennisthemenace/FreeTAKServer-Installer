import subprocess
import os
import getpass
VERSION = "0.2.2"


def add_to_cron():
    try:
        from crontab import CronTab
    except ImportError:
        subprocess.run(["pip3", "install", "python-crontab"], capture_output=True)
    from crontab import CronTab
    try:
        cron = CronTab(user=getpass.getuser())
        job = cron.new(command='nohup sudo python3 -m FreeTAKServer.controllers.services.FTS &')
        job.every_reboot()
        cron.write()
    except Exception:
        return 1
    return 0


def install_pip():
    subprocess.run(["apt", "autoremove", "-y"], capture_output=True)
    pip = subprocess.run(["apt", "install", "python3-pip", "-y"], capture_output=True)
    print(pip)
    return pip.returncode


def install_fts():
    pip = subprocess.run(["pip3", "install", "FreeTAKServer==1.3.0.6"], capture_output=True)
    print(pip)
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
                           "python3-lxml", "libcairo2-dev", "-y"], capture_output=True)
    print(pylibs)
    return pylibs.returncode


def install_pip_modules():
    pip = subprocess.run(["pip3", "install", "wheel"], capture_output=True)
    print(pip)
    return pip.returncode


def install_service():
    system_d_file_template = """[Unit]
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
    """

    with open('/etc/systemd/system/FreeTAKServer.service', 'w') as service_file:
        service_file.write(system_d_file_template)

    subprocess.run(["systemctl", "enable", "FreeTAKServer.service"], capture_output=True)
    sysd = subprocess.run(["systemctl", "start", "FreeTAKServer.service"], capture_output=True)
    return sysd.returncode


if __name__ == '__main__':
    print("Installing python3 pip")
    if install_pip() != 0:
        print("Something went wrong!")
        exit(1)
    print("------------------------------")
    print("Installing python libraries")
    if install_python_libraries() != 0:
        print("Something went wrong!")
        exit(1)
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
    # print("Installing FreeTAKServer as a systemd service")
    # if install_service() != 0:
    #     print("Something went wrong!")
    #     exit(1)
    # print("------------------------------")
    print("Adding FreeTAKServer as a cron job")
    if add_to_cron() != 0:
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
