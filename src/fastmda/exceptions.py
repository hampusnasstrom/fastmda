from types import ModuleType

from fastmda.schemas import ActuatorInfo, DeviceType, SettingInfo


class FastMDAException(Exception):
    """
    Super class for all FastMDA exceptions
    """
    pass


class FastMDAConnectFailed(FastMDAException):
    """
    Raised if a device fails to connect
    """

    def __init__(self, device: DeviceType, device_id: int, message: str = ""):
        """
        Init method for FastMDAConnectFailed exception.

        :param device: The device type that failed to connect.
        :type device: DeviceType
        :param device_id: The unique ID of the device that failed to connect.
        :type device_id: int
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'The {device.name} device with id {device_id} failed to connect. {message}'
        super().__init__(self.message)


class FastMDADisconnectFailed(FastMDAException):
    """
    Raised if a device fails to disconnect
    """

    def __init__(self, device: DeviceType, device_id: int, message: str = ""):
        """
        Init method for FastMDADisconnectFailed exception.

        :param device: The device type that failed to disconnect.
        :type device: DeviceType
        :param device_id: The unique ID of the device that failed to disconnect.
        :type device_id: int
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'The {device.name} device with id {device_id} failed to disconnect. {message}'
        super().__init__(self.message)


class FastMDAImplementationError(FastMDAException):
    """
    Raised if a device or measurement is not written according to specification
    """

    def __init__(self, implemented_module: ModuleType, message: str = ""):
        """
        Init method for FastMDAImplementationError exception

        :param implemented_module: The module that is not implemented according to specification.
        :type implemented_module: ModuleType
        :param message: Detailed message for log.
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
        Init method for FastMDAImplementationError exception.

        :param implemented_module: The module that cannot be found.
        :type implemented_module: str
        :param message: Detailed message for log.
        :type message: str
        """
        self.message = f'No {implemented_module} module found. {message}'
        super().__init__(self.message)


class FastMDAatSoftwareLimit(FastMDAException):
    """
    Raised if an actuator is at its software limit.
    """

    def __init__(self, actuator_info: ActuatorInfo, message: str = ""):
        """
        Init method for FastMDAatSoftwareLimit exception.

        :param actuator_info: The ActuatorInfo object of the actuator at the limit.
        :type actuator_info: ActuatorInfo
        :param message: Detailed message for log.
        :type message: str
        """
        self.message = f'Actuator {actuator_info.name} with id {actuator_info.actuator_id} of device' + \
                       f'{actuator_info.device_id} at software limit. {message}'
        super().__init__(self.message)


class FastMDAatHardwareLimit(FastMDAException):
    """
    Raised if an actuator is at its hardware limit.
    """

    def __init__(self, actuator_info: ActuatorInfo, message: str = ""):
        """
        Init method for FastMDAatHardwareLimit exception.

        :param actuator_info: The ActuatorInfo object of the actuator at the limit
        :type actuator_info: ActuatorInfo
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'Actuator {actuator_info.name} with id {actuator_info.actuator_id} of device' + \
                       f'{actuator_info.device_id} at hardware limit. {message}'
        super().__init__(self.message)


class FastMDAatHardSettingLimit(FastMDAException):
    """
    Raised if a setting is at its hard limit.
    """

    def __init__(self, setting_info: SettingInfo, message: str = ""):
        """
        Init method for FastMDAatHardSettingLimit exception.

        :param setting_info: The ActuatorType object of the actuator at the limit
        :type setting_info: ActuatorType
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'Setting {setting_info.name} with ID {setting_info.actuator_id} with parent ID' + \
                       f'{setting_info.parent_id} (with possible grandparent ID {setting_info.grandparent_id}) ' + \
                       f'at hard limit. {message}'
        super().__init__(self.message)


class FastMDAatSoftSettingLimit(FastMDAException):
    """
    Raised if a setting is at its soft limit.
    """

    def __init__(self, setting_info: SettingInfo, message: str = ""):
        """
        Init method for FastMDAatSoftSettingLimit exception.

        :param setting_info: The ActuatorType object of the actuator at the limit
        :type setting_info: ActuatorType
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'Setting {setting_info.name} with ID {setting_info.actuator_id} with parent ID' + \
                       f'{setting_info.parent_id} (with possible grandparent ID {setting_info.grandparent_id}) ' + \
                       f'at soft limit. {message}'
        super().__init__(self.message)


class FastMDAisBusy(FastMDAException):
    """
    Raised if a value cannot be set or data cannot be acquired because the device is busy.
    """

    def __init__(self, device_id: int, message: str = ""):
        """
        Init method for the FastMDAisBusy exception

        :param device_id: The unique ID of the device that is busy.
        :type device_id: int
        :param message: Detailed message for log.
        :type message: str
        """
        self.message = f'Device with ID {device_id} is busy. {message}'
        super().__init__(self.message)
