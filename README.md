# ot2-controller

A [SiLA 2](https://sila-standard.com/) compliant controller for an Opentrons [OT-2 Liquid Handler](https://opentrons.com/ot-2/).
For a short function overview, and a description on how to use this software, take a look into the [User Guide](doc/UserGuide.md).

## Requirements

**1. Install the [sila2lib](https://gitlab.com/SiLA2/legacy/sila_python_20211115/-/tree/feature/silacodegenerator-0.3) library in version 0.3 or higher:**  
Ensure the `python3-distutils` and `python3-pip` packages are installed (install with `sudo apt install <package>` if not).
```
git clone --recursive https://gitlab.com/SiLA2/legacy/sila_python_20211115
git -C sila_python_20211115 checkout feature/silacodegenerator-0.3
pip install sila_python_20211115/sila_library/
```
Follow further with the installation instructions described at the [sila2lib repository](https://gitlab.com/SiLA2/legacy/sila_python_20211115).

**2. Clone this git repository:**
```
git clone https://github.com/FlorianBauer/ot2-controller
cd ot2-controller
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

**5. Upgrade protobuf (just to be sure):**
```
pip install --upgrade protobuf
```

**6. Establish a SSH connection:**  
Before the actual installation, a SSH connection to the OT-2 device has to be established.
This requires to generate a pair of SSH keys, as well as the configuration of the OT-2 device 
itself. To do this, please follow the steps described in this article:
[SSH for OT-2](https://support.opentrons.com/en/articles/3203681-setting-up-ssh-access-to-your-ot-2)


## Installation

Use the generated key from step 6 and register it on the client.
```bash
sudo ssh-copy-id -i ~/.ssh/ot2_ssh_key `whoami`@`hostname`
# e.g. sudo ssh-copy-id -i ~/.ssh/ot2_ssh_key username@my_host.org
```
Ensure the packages `openssh-server` and `openssh-client` are installed. If not, install with 
`apt install openssh-server openssh-client`.

_Some additional useful links for troubleshooting:_
* https://hackersandslackers.com/automate-ssh-scp-python-paramiko/
* https://askubuntu.com/questions/685890/ssh-connect-t-host-slave-1-port-22-connection-refused

## Start the Server

Now execute the `Ot2Controller_server.py` script with the corresponding OT-2 device IP (e.g. with 
`python3 OtController_server.py -a 169.254.92.42`).

The SiLA server should now be available on localhost (`127.0.0.1`) on the port `50064`.

Terminate the server with **[Ctrl]+[c]** or by typing `stop` into the running terminal window.

A more detailed description can be found in the [User Guide](doc/UserGuide.md).


## General Remarks

The SiLA server is currently only able to run on a host computer which has to be connected to 
the OT-2 device via SSH. Since the OT-2 robot itself is also running a Linux OS on its 
[build-in Raspberry Pi 3+](https://support.opentrons.com/en/articles/2715311-integrating-the-ot-2-with-other-lab-equipment), 
it may be possible to install the SiLA server and the corresponding 
[sila_python](https://gitlab.com/SiLA2/legacy/sila_python_20211115#installation) libraries on to the OT-2 directly. 
Pull requests and instructions regarding this are gladly welcome.
