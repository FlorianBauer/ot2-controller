"""
________________________________________________________________________

:PROJECT: SiLA2_python

*OT-2 Controller*

:details: Ot2Controller:
    A SiLA 2 complaint controller for an OT-2 Liquid Handler robot.
           
:file:    Ot2Controller_servicer.py
:authors: Florian Bauer <florian.bauer.dev@gmail.com>

:date: (creation)          2020-09-10T19:34:31.281020
:date: (last modification) 2020-09-10T19:34:31.281020

.. note:: Code generated by sila2codegenerator 0.2.0

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.0.1"

# import general packages
import logging
import grpc

# meta packages
from typing import Union

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
from sila2lib.error_handling.server_err import SiLAError

# import gRPC modules for this feature
from .gRPC import Ot2Controller_pb2 as Ot2Controller_pb2
from .gRPC import Ot2Controller_pb2_grpc as Ot2Controller_pb2_grpc

# import simulation and real implementation
from .Ot2Controller_simulation import Ot2ControllerSimulation
from .Ot2Controller_real import Ot2ControllerReal


class Ot2Controller(Ot2Controller_pb2_grpc.Ot2ControllerServicer):
    """
    A SiLA 2 service enabling the execution of python protocols on a Opentrons 2 liquid handler robot.
    """
    implementation: Union[Ot2ControllerSimulation, Ot2ControllerReal]
    simulation_mode: bool

    def __init__(self, simulation_mode: bool = True):
        """
        Class initialiser.

        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """

        self.simulation_mode = simulation_mode
        if simulation_mode:
            self._inject_implementation(Ot2ControllerSimulation())
        else:
            self._inject_implementation(Ot2ControllerReal())

    def _inject_implementation(self,
                               implementation: Union[Ot2ControllerSimulation,
                                                     Ot2ControllerReal]
                               ) -> bool:
        """
        Dependency injection of the implementation used.
            Allows to set the class used for simulation/real mode.

        :param implementation: A valid implementation of the Ot2ControllerServicer.
        """

        self.implementation = implementation
        return True

    def switch_to_simulation_mode(self):
        """Method that will automatically be called by the server when the simulation mode is requested."""
        self.simulation_mode = True
        self._inject_implementation(Ot2ControllerSimulation())

    def switch_to_real_mode(self):
        """Method that will automatically be called by the server when the real mode is requested."""
        self.simulation_mode = False
        self._inject_implementation(Ot2ControllerReal())

    def UploadProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.UploadProtocol_Responses:
        """
        Executes the unobservable command "Upload Protocol"
            Uploads the given Protocol to the "/data/user_storage" dir on the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolSourcePath (Protocol Source Path): The path to the Protocol to upload.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        logging.debug(
            "UploadProtocol called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
    
        try:
            return self.implementation.UploadProtocol(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)
    
    def RemoveProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.RemoveProtocol_Responses:
        """
        Executes the unobservable command "Remove Protocol"
            Removes the given Protocol from the "/data/user_storage" dir on the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolFile (Protocol File): The file name of the Protocol to remove.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """
    
        logging.debug(
            "RemoveProtocol called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
    
        try:
            return self.implementation.RemoveProtocol(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)
    
    def RunProtocol(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.RunProtocol_Responses:
        """
        Executes the unobservable command "Run Protocol"
            Runs the given Protocol on the OT-2.
    
        :param request: gRPC request containing the parameters passed:
            request.ProtocolFile (Protocol File): The file name of the Protocol to run.
            request.IsSimulating (Is Simulating): Defines whether the protocol gets just simulated or actually executed on the device.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: The return object defined for the command with the following fields:
            request.ReturnValue (Return Value): The returned value from the executed protocol. On a simulated execution, only the value 0
            is indicating a successful simulation.
        """
    
        logging.debug(
            "RunProtocol called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
    
        try:
            return self.implementation.RunProtocol(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)

    def Get_Connection(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_Connection_Responses:
        """
        Requests the unobservable property Connection
            Connection details of the remote OT-2.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.Connection (Connection): Connection details of the remote OT-2.
        """
    
        logging.debug(
            "Property Connection requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.Get_Connection(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)
    
    def Get_AvailableProtocols(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_AvailableProtocols_Responses:
        """
        Requests the unobservable property Available Protocols
            List of the stored files available on the OT-2.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.AvailableProtocols (Available Protocols): List of the stored files available on the OT-2.
        """
    
        logging.debug(
            "Property AvailableProtocols requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.Get_AvailableProtocols(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)
    
    def Get_AvailableJupyterNotebooks(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_AvailableJupyterNotebooks_Responses:
        """
        Requests the unobservable property Available Jupyter Notebooks
            List of the stored Jupyter Notebooks available on the OT-2.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.AvailableJupyterNotebooks (Available Jupyter Notebooks): List of the stored Jupyter Notebooks available on the OT-2.
        """
    
        logging.debug(
            "Property AvailableJupyterNotebooks requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.Get_AvailableJupyterNotebooks(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)
    
    def Get_CameraPicture(self, request, context: grpc.ServicerContext) \
            -> Ot2Controller_pb2.Get_CameraPicture_Responses:
        """
        Requests the unobservable property Camera Picture
            A current picture from the inside of the OT-2 made with the built-in camera.
    
        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information
    
        :returns: A response object with the following fields:
            request.CameraPicture (Camera Picture): A current picture from the inside of the OT-2 made with the built-in camera.
        """
    
        logging.debug(
            "Property CameraPicture requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.Get_CameraPicture(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)
