# User Guide
This guide provides a short descriptions of the available functionalities of the ot2-controller and how to use them. Instructions on how to install the software can be found in the [README](../README.md).

## Feature Overview
OT-2 Controller Feature  

Properties:
- **Available Protocols**: Lists all available python protocols installed on the OT-2 device.
- **Camera Picture**: Takes a current picture (*.jpeg) from the deck with the build-in camera.
- **Connection**: Shows some details about the Connection (e.g. IP-Address and  SSH-key fingerprint).
  
Commands:
- **Upload Protocol**: Uploads a given protocol from the host on the device. Therefore, the path to the python file on the host must be given (e.g. `/home/user/my_protocol.py`).
- **Run Protocol**: Runs (or simulates the run) of the given protocol. Therefore, the name of the uploaded file must be given including the `.py` suffix (e.g. `my_protocol.py`).
- **Remove Protocol**: Removes the uploaded file from the device (e.g. `my_protocl.py`).

## Server Start-Up
Ensure all installation steps as described in the [README](../README.md) were completed before you continue.

1. Turn on the OT-2 (obviously).  

2. Establish a network connection to the OT-2:  
This can be achieved via the Opentrons App. Thereby, it doesn't matter if the device is connected via [USB](https://support.opentrons.com/en/articles/2687586-get-started-connect-to-your-ot-2-over-usb) or [Wi-Fi](https://support.opentrons.com/en/articles/2687573-get-started-connect-to-your-ot-2-over-wi-fi-optional).

3. Start the SiLA-Server:  
To start-up the server, the IP-Address of the OT-2 must be given via the `-o/--ot2-ip-address` argument. The Address can be looked up in the Opentrons App. It is recommended to [set a static IP-Address](https://support.opentrons.com/en/articles/2934336-manually-adding-a-robot-s-ip-address), otherwise the IP-Address may change on every device restart. 

Now, start the server with the actual IP-Address.
```
# If working with an virtual environment, don't forget to export the environment variables first.
# source path/to/venv/bin/activate
python3 -m ot2_controller -o 169.254.92.42
```

The SiLA server should now be available on localhost (`127.0.0.1`) on the default port `50064`.
Use `-a/--ip-address IP` and `-p/--port PORT` to explicitly set the host address. 

A universal SiLA 2 client to inspect and test the available service(s) can be found here:
[sila-orchestrator](https://github.com/FlorianBauer/sila-orchestrator)

To terminate the server, press the Enter key in the running terminal window.

**Troubleshooting:**
If no connection to the SiLA server could be established, check if the [SSH Keys](https://support.opentrons.com/en/articles/3203681-setting-up-ssh-access-to-your-ot-2) are properly installed on the OT-2 and the SiLA server host.

## Server Arguments
See `python3 -m ot2_controller --help` for a full list:

```
usage: ot2-controller [-h] -o OT2_IP_ADDRESS [-a IP_ADDRESS] [-p PORT]
                      [--server-uuid SERVER_UUID] [--disable-discovery]
                      [--insecure] [-k PRIVATE_KEY_FILE] [-c CERT_FILE]
                      [--ca-export-file CA_EXPORT_FILE] [-q | -v | -d]

Start this SiLA 2 server

optional arguments:
  -h, --help            show this help message and exit
  -o OT2_IP_ADDRESS, --ot2-ip-address OT2_IP_ADDRESS
                        The IP address of the Opentrons OT-2 system
  -a IP_ADDRESS, --ip-address IP_ADDRESS
                        The IP address (default: '127.0.0.1')
  -p PORT, --port PORT  The port (default: 50064)
  --server-uuid SERVER_UUID
                        The server UUID (default: create random UUID)
  --disable-discovery   Disable SiLA Server Discovery
  --insecure            Start without encryption
  -k PRIVATE_KEY_FILE, --private-key-file PRIVATE_KEY_FILE
                        Private key file (e.g. 'server-key.pem')
  -c CERT_FILE, --cert-file CERT_FILE
                        Certificate file (e.g. 'server-cert.pem')
  --ca-export-file CA_EXPORT_FILE
                        When using a self-signed certificate, write the
                        generated CA to this file
  -q, --quiet           Only log errors
  -v, --verbose         Enable verbose logging
  -d, --debug           Enable debug logging
```

## Using Protocols
This requires installation of the [Opentrons Python library](https://pypi.org/project/opentrons/): `pip install opentrons`. 
Since the Python protocols are executed directly on the robot hardware, the initial calibration steps are omitted. Incorrect positioning of the pipettes may be the consequence. To avoid this, it is possible to set the desired calibration offsets manually within the protocol. Therefore, the offset values must be gathered empirically through testing or can be extracted from the *.json file exported from the Opentrons App itself (see picture).

![Export OT-2 calibration data](pics/ExportCalibration.png)

The following example shows how the offset values are used in the protocol:

```python
# ...
from opentrons.types import Point
# ...

# The used offsets are defined here. The concrete values can be gathered manually or copied from
# an existing file (e.g. from the *.json file exported from the Opentrons App).
OFFSET_RIGHT_MOUNT = Point(x=1.24, y=2.4, z=-0.6) # offset values in mm
OFFSET_LEFT_MOUNT = Point(x=-1.67, y=-0.1, z=2.0)

def run(protocol: protocol_api.ProtocolContext):
    # Load tiprack and set the slot location.
    tiprack1 = protocol.load_labware('opentrons_96_filtertiprack_200ul', 1)

    # Apply the offset.
    tiprack1.set_calibration(OFFSET_RIGHT_MOUNT)  

    # All other labware affected by the corresponding mount shall be adjusted with `set_callibration` as well.
    # ...
```
