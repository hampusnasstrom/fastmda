from types import ModuleType

from fastmda.schemas import ActuatorInfo, DeviceType


class FastMDAException(Exception):
    """
    Super class for all FastMDA exceptions
    """
    pass


class FastMDAConnectFailed(FastMDAException):
    """
    Raised if a device fails to connect
    """

    def __init__(self, device: DeviceType, message: str = ""):
        """
        Init method for FastMDAConnectFailed exception

        :param device: The device that failed to connect
        :type device: Device
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'A {device.name} device failed to connect. {message}'
        super().__init__(self.message)


class FastMDAImplementationError(FastMDAException):
    """
    Raised if a device or measurement is not written according to specification
    """

    def __init__(self, implemented_module: ModuleType, message: str = ""):
        """
        Init method for FastMDAImplementationError exception

        :param implemented_module: The module that is not implemented according to specification
        :type implemented_module: ModuleType
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'{implemented_module.__name__} not implemented according to spec. {message}'
        super().__init__(self.message)


class FastMDAModuleError(FastMDAException):
    """
    Raised if a module cannot be found
    """

    def __init__(self, implemented_module: str, message: str = ""):
        """
        Init method for FastMDAImplementationError exception

        :param implemented_module: The module that cannot be found
        :type implemented_module: str
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'No {implemented_module} module found. {message}'
        super().__init__(self.message)


class FastMDAatSoftwareLimit(FastMDAException):
    """
    Raised if an actuator is at it's software limit.
    """

    def __init__(self, actuator_info: ActuatorInfo, message: str = ""):
        """
        Init method for FastMDAatSoftwareLimit exception

        :param actuator_info: The ActuatorInfo object of the actuator at the limit
        :type actuator_info: ActuatorInfo
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'Actuator {actuator_info.name} at software limit. {message}'
        super().__init__(self.message)
