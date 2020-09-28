# ot2-controller

A [SiLA 2](https://sila-standard.com/) complaint controller for an Opentrons 
[OT-2 Liquid Handler](https://opentrons.com/ot-2/) robot.


## Requirements

1. The underlying SiLA library has to be installed: 
[sila_python](https://gitlab.com/SiLA2/sila_python#installation)
2. A SSH connection has to be established: 
[SSH for OT-2](https://support.opentrons.com/en/articles/3203681-setting-up-ssh-access-to-your-ot-2)


## Installation

Use the generated key from step 2 and register it on the client (may require `sudo` privileges).
```
ssh-copy-id -i ~/.ssh/ot2_ssh_key `whoami`@`hostname`
# e.g. sudo ssh-copy-id -i ~/.ssh/ot2_ssh_key username@my_host.org
```
Ensure the package `openssh-server` is installed. If not, install with `apt install openssh-server`.

_Some additional useful links for troubleshooting:_
* https://hackersandslackers.com/automate-ssh-scp-python-paramiko/
* https://askubuntu.com/questions/685890/ssh-connect-t-host-slave-1-port-22-connection-refused

To add default encryption, generate a sefl-signed certificate:
```
openssl req -x509 -newkey rsa:4096 -keyout sila_server.key -out sila_server.crt -days 365 -subj '/CN=localhost' -nodes
```

Place the two files `sila_server.crt` and a `sila_server.key` in the same directory as the Python server and they get 
selected on start-up by default.


## Start the Server

Now execute the `Ot2Controller_server.py` script (e.g. 
with `python3 -m /path/to/ot2-controller/OtController_server.py`).

The server should now be available on localhost (`127.0.0.1`) on the port `50053`.

Terminate the server with **[Ctrl]+[c]** or by typing `stop` into the opened terminal window.


## General Remarks

The SiLA server is currently only able to run on a host computer which has to be connected to 
the OT-2 device via SSH. Since the OT-2 robot itself is also running a Linux OS on its 
[build-in Raspberry Pi 3+](https://support.opentrons.com/en/articles/2715311-integrating-the-ot-2-with-other-lab-equipment)
, it may be possible to install the SiLA server on the OT-2 directly.
