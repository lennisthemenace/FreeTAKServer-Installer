# FreeTAKServer-Installer
Python based installer script for FreeTAKServer

This tool is to make installing FreeTAKServer a one liner

Just run:

`curl -L https://git.io/JLSRp > install.py ; sudo python3 install.py`

Finally, reboot:

`sudo reboot`


This has been tested on RaspberryOS and Ubuntu 20.04

This should:
1. Make sure you have everything you need on the machine
2. Install FreeTAKServer + UI
3. Adds FreeTAKServer to cron to make sure FTS runs automatically
4. Create a symlink folder at ~/FTS which links to the main FreeTAKServer folder
5. Create a symlink folder at ~/FTS-UI which links to the main FreeTAKServer-UI folder
