#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*Ot2Controller client*

:details: Ot2Controller:
    A SiLA 2 service enabling the execution of python protocols on a Opentrons 2 liquid handler robot.

:file:    Ot2Controller_client.py
:authors: Florian Bauer <florian.bauer.dev@gmail.com>

:date: (creation)          2020-08-22T22:14:39.138850
:date: (last modification) 2020-08-22T22:14:39.138850

.. note:: Code generated by sila2codegenerator 0.2.0

_______________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.0.1"

# import general packages
import logging
import argparse
import grpc
import time

# import meta packages
from typing import Union, Optional

# import SiLA2 library modules
from sila2lib.framework import SiLAFramework_pb2 as silaFW_pb2
from sila2lib.sila_client import SiLA2Client
from sila2lib.framework.std_features import SiLAService_pb2 as SiLAService_feature_pb2
from sila2lib.error_handling import client_err
#   Usually not needed, but - feel free to modify
# from sila2lib.framework.std_features import SimulationController_pb2 as SimController_feature_pb2

# import feature gRPC modules
# Import gRPC libraries of features
from Ot2Controller.gRPC import Ot2Controller_pb2
from Ot2Controller.gRPC import Ot2Controller_pb2_grpc
# import default arguments for this feature
from Ot2Controller.Ot2Controller_default_arguments import default_dict as Ot2Controller_default_dict


# noinspection PyPep8Naming, PyUnusedLocal
class Ot2ControllerClient(SiLA2Client):
    """
        A SiLA 2 service enabling the execution of python protocols on a Opentrons 2 liquid handler robot.

    .. note:: For an example on how to construct the parameter or read the response(s) for command calls and properties,
              compare the default dictionary that is stored in the directory of the corresponding feature.
    """
    # The following variables will be filled when run() is executed
    #: Storage for the connected servers version
    server_version: str = ''
    #: Storage for the display name of the connected server
    server_display_name: str = ''
    #: Storage for the description of the connected server
    server_description: str = ''

    def __init__(self,
                 name: str = "Ot2ControllerClient", description: str = "A SiLA 2 service enabling the execution of python protocols on a Opentrons 2 liquid handler robot.",
                 server_name: Optional[str] = None,
                 client_uuid: Optional[str] = None,
                 version: str = __version__,
                 vendor_url: str = "https://www.cs7.tf.fau.de",
                 server_hostname: str = "localhost", server_ip: str = "127.0.0.1", server_port: int = 50053,
                 cert_file: Optional[str] = None):
        """Class initialiser"""
        super().__init__(
            name=name, description=description,
            server_name=server_name,
            client_uuid=client_uuid,
            version=version,
            vendor_url=vendor_url,
            server_hostname=server_hostname, server_ip=server_ip, server_port=server_port,
            cert_file=cert_file
        )

        logging.info(
            "Starting SiLA2 service client for service Ot2Controller with service name: {server_name}".format(
                server_name=name
            )
        )

        # Create stub objects used to communicate with the server
        self.Ot2Controller_stub = \
            Ot2Controller_pb2_grpc.Ot2ControllerStub(self.channel)

        # initialise class variables for server information storage
        self.server_version = ''
        self.server_display_name = ''
        self.server_description = ''

    def Get_ImplementedFeatures(self):
        """Get a list of all implemented features."""
        # type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Retrieving the list of implemented features of the server:")
        try:
            response = self.SiLAService_stub.Get_ImplementedFeatures(
                SiLAService_feature_pb2.Get_ImplementedFeatures_Parameters()
            )
            for feature_id in response.ImplementedFeatures:
                logging.debug("Implemented feature: {feature_id}".format(
                    feature_id=feature_id.value)
                    )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

        return response.ImplementedFeatures

    def Get_FeatureDefinition(self, feature_identifier: str) -> Union[str, None]:
        """
        Returns the FDL/XML feature definition of the given feature.

        :param feature_identifier: The name of the feature for which the definition should be returned.
        """
        # type definition, just for convenience
        grpc_err: grpc.Call

        logging.debug("Requesting feature definitions of feature {feature_identifier}:".format(
            feature_identifier=feature_identifier)
        )
        try:
            response = self.SiLAService_stub.GetFeatureDefinition(
                SiLAService_feature_pb2.GetFeatureDefinition_Parameters(
                    QualifiedFeatureIdentifier=silaFW_pb2.String(value=feature_identifier)
                    )
                )
            logging.debug("Response of GetFeatureDefinition for {feature_identifier} feature: {response}".format(
                response=response,
                feature_identifier=feature_identifier)
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None

    def run(self) -> bool:
        """
        Starts the actual client and retrieves the meta-information from the server.

        :returns: True or False whether the connection to the server is established.
        """
        # type definition, just for convenience
        grpc_err: grpc.Call

        try:
            # Retrieve the basic server information and store it in internal class variables
            #   Display name
            response = self.SiLAService_stub.Get_ServerName(SiLAService_feature_pb2.Get_ServerName_Parameters())
            self.server_display_name = response.ServerName.value
            logging.debug("Display name: {name}".format(name=response.ServerName.value))
            # Server description
            response = self.SiLAService_stub.Get_ServerDescription(
                SiLAService_feature_pb2.Get_ServerDescription_Parameters()
            )
            self.server_description = response.ServerDescription.value
            logging.debug("Description: {description}".format(description=response.ServerDescription.value))
            # Server version
            response = self.SiLAService_stub.Get_ServerVersion(SiLAService_feature_pb2.Get_ServerVersion_Parameters())
            self.server_version = response.ServerVersion.value
            logging.debug("Version: {version}".format(version=response.ServerVersion.value))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return False

        return True

    def stop(self, force: bool = False) -> bool:
        """
        Stop SiLA client routine

        :param force: If set True, the client is supposed to disconnect and stop immediately. Otherwise it can first try
                      to finish what it is doing.

        :returns: Whether the client could be stopped successfully or not.
        """
        # TODO: Implement all routines that have to be executed when the client is stopped.
        #   Feel free to use the "force" parameter to abort any running processes. Or crash your machine. Your call!
        return True

    def UploadProtocol(self,
                      parameter: Ot2Controller_pb2.UploadProtocol_Parameters = None) \
            -> Ot2Controller_pb2.UploadProtocol_Responses:
        """
        Wrapper to call the unobservable command UploadProtocol on the server.
    
        :param parameter: The parameter gRPC construct required for this command.
    
        :returns: A gRPC object with the response that has been defined for this command.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call
    
        logging.debug("Calling UploadProtocol:")
        try:
            # resolve to default if no value given
            #   TODO: Implement a more reasonable default value
            if parameter is None:
                parameter = Ot2Controller_pb2.UploadProtocol_Parameters(
                    **Ot2Controller_default_dict['UploadProtocol_Parameters']
                )
    
            response = self.Ot2Controller_stub.UploadProtocol(parameter)
    
            logging.debug('UploadProtocol response: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None
    
        return response
    
    def RemoveProtocol(self,
                      parameter: Ot2Controller_pb2.RemoveProtocol_Parameters = None) \
            -> Ot2Controller_pb2.RemoveProtocol_Responses:
        """
        Wrapper to call the unobservable command RemoveProtocol on the server.
    
        :param parameter: The parameter gRPC construct required for this command.
    
        :returns: A gRPC object with the response that has been defined for this command.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call
    
        logging.debug("Calling RemoveProtocol:")
        try:
            # resolve to default if no value given
            #   TODO: Implement a more reasonable default value
            if parameter is None:
                parameter = Ot2Controller_pb2.RemoveProtocol_Parameters(
                    **Ot2Controller_default_dict['RemoveProtocol_Parameters']
                )
    
            response = self.Ot2Controller_stub.RemoveProtocol(parameter)
    
            logging.debug('RemoveProtocol response: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None
    
        return response
    
    def RunProtocol(self,
                      parameter: Ot2Controller_pb2.RunProtocol_Parameters = None) \
            -> Ot2Controller_pb2.RunProtocol_Responses:
        """
        Wrapper to call the unobservable command RunProtocol on the server.
    
        :param parameter: The parameter gRPC construct required for this command.
    
        :returns: A gRPC object with the response that has been defined for this command.
        """
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call
    
        logging.debug("Calling RunProtocol:")
        try:
            # resolve to default if no value given
            #   TODO: Implement a more reasonable default value
            if parameter is None:
                parameter = Ot2Controller_pb2.RunProtocol_Parameters(
                    **Ot2Controller_default_dict['RunProtocol_Parameters']
                )
    
            response = self.Ot2Controller_stub.RunProtocol(parameter)
    
            logging.debug('RunProtocol response: {response}'.format(response=response))
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None
    
        return response
    

    def Get_Connection(self) \
            -> Ot2Controller_pb2.Get_Connection_Responses:
        """Wrapper to get property Connection from the server."""
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call
    
        logging.debug("Reading unobservable property Connection:")
        try:
            response = self.Ot2Controller_stub.Get_Connection(
                Ot2Controller_pb2.Get_Connection_Parameters()
            )
            logging.debug(
                'Get_Connection response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None
    
        return response
    def Get_AvailableProtocols(self) \
            -> Ot2Controller_pb2.Get_AvailableProtocols_Responses:
        """Wrapper to get property AvailableProtocols from the server."""
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call
    
        logging.debug("Reading unobservable property AvailableProtocols:")
        try:
            response = self.Ot2Controller_stub.Get_AvailableProtocols(
                Ot2Controller_pb2.Get_AvailableProtocols_Parameters()
            )
            logging.debug(
                'Get_AvailableProtocols response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None
    
        return response
    def Get_AvailableJupyterNotebooks(self) \
            -> Ot2Controller_pb2.Get_AvailableJupyterNotebooks_Responses:
        """Wrapper to get property AvailableJupyterNotebooks from the server."""
        # noinspection PyUnusedLocal - type definition, just for convenience
        grpc_err: grpc.Call
    
        logging.debug("Reading unobservable property AvailableJupyterNotebooks:")
        try:
            response = self.Ot2Controller_stub.Get_AvailableJupyterNotebooks(
                Ot2Controller_pb2.Get_AvailableJupyterNotebooks_Parameters()
            )
            logging.debug(
                'Get_AvailableJupyterNotebooks response: {response}'.format(
                    response=response
                )
            )
        except grpc.RpcError as grpc_err:
            self.grpc_error_handling(grpc_err)
            return None
    
        return response
    

    @staticmethod
    def grpc_error_handling(error_object: grpc.Call) -> None:
        """Handles exceptions of type grpc.RpcError"""
        # pass to the default error handling
        grpc_error =  client_err.grpc_error_handling(error_object=error_object)

        # Access more details using the return value fields
        # grpc_error.message
        # grpc_error.error_type


def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 client: Ot2Controller")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    return parser.parse_args()


if __name__ == '__main__':
    # or use logging.INFO (=20) or logging.ERROR (=30) for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    parsed_args = parse_command_line()

    # start the server
    sila_client = Ot2ControllerClient(server_ip='127.0.0.1', server_port=50053)
    sila_client.run()

    # Log connection info
    logging.info(
        (
            'Connected to SiLA Server {display_name} running in version {version}.' '\n'
            'Service description: {service_description}'
        ).format(
            display_name=sila_client.server_display_name,
            version=sila_client.server_version,
            service_description=sila_client.server_description
        )
    )

    # TODO:
    #   Write your further function calls here to run the client as a standalone application.
