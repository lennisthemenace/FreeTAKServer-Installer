# FreeTAKServer-Installer
Python based installer script for FreeTAKServer

This tool is to make installing FreeTAKServer a one liner

Just run:

`curl -L https://git.io/JLSRp | sudo python3 -`

Then run the atakofthecerts script from [here](https://github.com/lennisthemenace/ATAK-Certs) to generate the needed certificate for FTS to run. (Changing the SERVER_IP for the ip address clients use for connecting):

`curl -L https://git.io/JL9DP | sudo python3 - -a -c -i SERVER_IP`

Finally, reboot:

`sudo reboot`

If you do not run the second command, FreeTAKServer will still be installed but there will be no 
Certificates loaded in to the server meaning that after 20 minutes, all clients will be kick from the server. 

This has been testing on RaspberryOS and Ubuntu 20.04

This should:
1. Make sure you have everything you need on the machine
2. Install FreeTAKServer
3. Adds FreeTAKServer to cron to make sure FTS runs automatically
4. Create a symlink folder at ~/FTS which links to the main FreeTAKServer folder
5. Generates and adds the necessary certificates to FTS and a data package called user.zip to import into clients