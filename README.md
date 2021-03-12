# ot2-controller

A [SiLA 2](https://sila-standard.com/) complaint controller for an Opentrons 
[OT-2 Liquid Handler](https://opentrons.com/ot-2/) robot.


## Requirements

**1. Install the [sila2lib](https://gitlab.com/SiLA2/sila_python/-/tree/feature/silacodegenerator-0.3) library in version 0.3 or higher:**  
Ensure the `python3-distutils` package is installed (install with `apt install python3-distutils` if not).
Checkout the newest version from the `feature/silacodegenerator-0.3` branch.
```
git clone https://gitlab.com/SiLA2/sila_python.git -b feature/silacodegenerator-0.3
```
Follow further with the installation instructions described at the [sila2lib repositroy](https://gitlab.com/SiLA2/sila_python/-/tree/feature/silacodegenerator-0.3#installation).

**2. Clone this git repository:**  
```
git clone https://github.com/FlorianBauer/ot2-controller.git
cd ot-controller
```

**3. (Optional) Set up and source a Python environment:**  
```
python3 -m venv ./venv
source venv/bin/activate
```

**4. Install dependant Python packages:**  
```
pip install -r requirements.txt
```

**5. Establish a SSH connection:**  
Before the actual installation, a SSH connection to the OT-2 device has to be established.
This requires to generate a pair of SSH keys, as well as the configuration of the OT-2 device 
itself. To do this, please follow the steps described in this article:
[SSH for OT-2](https://support.opentrons.com/en/articles/3203681-setting-up-ssh-access-to-your-ot-2)


## Installation

Use the generated key from step 3 and register it on the client (may require `sudo` privileges).
```
ssh-copy-id -i ~/.ssh/ot2_ssh_key `whoami`@`hostname`
# e.g. sudo ssh-copy-id -i ~/.ssh/ot2_ssh_key username@my_host.org
```
Ensure the packages `openssh-server` and `openssh-client` are installed. If not, install with 
`apt install openssh-server openssh-client`.

_Some additional useful links for troubleshooting:_
* https://hackersandslackers.com/automate-ssh-scp-python-paramiko/
* https://askubuntu.com/questions/685890/ssh-connect-t-host-slave-1-port-22-connection-refused

_Optional:_ To add default encryption, generate a self-signed certificate:
```
openssl req -x509 -newkey rsa:4096 -keyout sila_server.key -out sila_server.crt -days 365 -subj '/CN=localhost' -nodes
```

Place the two files `sila_server.crt` and a `sila_server.key` in the same directory as the Python 
server, and they get selected on start-up by default.


## Start the Server

Now execute the `Ot2Controller_server.py` script with the corresponding OT-2 device IP (e.g. with 
`python3 -m /path/to/ot2-controller/OtController_server.py -a 169.254.92.42`).

The SiLA server should now be available on localhost (`127.0.0.1`) on the port `50064`.

Terminate the server with **[Ctrl]+[c]** or by typing `stop` into the running terminal window.


## General Remarks

The SiLA server is currently only able to run on a host computer which has to be connected to 
the OT-2 device via SSH. Since the OT-2 robot itself is also running a Linux OS on its 
[build-in Raspberry Pi 3+](https://support.opentrons.com/en/articles/2715311-integrating-the-ot-2-with-other-lab-equipment), 
it may be possible to install the SiLA server and the corresponding 
[sila_python](https://gitlab.com/SiLA2/sila_python#installation) libraries on to the OT-2 directly. 
Pull requests and instructions regarding this are gladly welcome.
