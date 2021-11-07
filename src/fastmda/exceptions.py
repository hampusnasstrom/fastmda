from fastmda.objects import AbstractDevice


class FastMDAException(Exception):
    """
    Super class for all FastMDA exceptions
    """
    pass


class FastMDAConnectFailed(FastMDAException):
    """
    Raised if a device fails to connect
    """

    def __init__(self, device: AbstractDevice, message: str = ""):
        """
        Init method for FastMDAConnectFailed exception

        :param device: The device that failed to connect
        :type device: Device
        :param message: Detailed message for log
        :type message: str
        """
        self.message = f'Device {device.id} failed to connect. {message}'
        super().__init__(self.message)
