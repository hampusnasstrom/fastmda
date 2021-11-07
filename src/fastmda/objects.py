from typing import List


class AbstractDetector:
    """
    Abstract class for the detector part of the device.
    """

    def __init__(self, dimensionality: int = 1):
        """
        Constructor for the super class

        :param dimensionality: The dimensionality of the detector, i.e. the dimension of the output array.
        :type dimensionality: int
        """
        self.dimensionality = dimensionality

    def acquire(self):
        raise NotImplementedError


class AbstractActuator:
    """
    Abstract class for the actuator part of the device.
    """

    def __init__(self):
        """
        Constructor of the Actuator class.
        """
        self.position = 0

    def get_position(self):
        raise NotImplementedError


class AbstractDevice:
    """
    Abstract class to be inherited by any device the controls the communication with actuators and/or detectors.
    """

    def __init__(self, device_id: str):
        """
        Constructor of the Device class.

        :param device_id: Unique id of the device.
        :type device_id: str
        """
        self.id = device_id

    def connect(self) -> bool:
        raise NotImplementedError

    def disconnect(self) -> bool:
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError

    def get_actuators(self) -> List[AbstractActuator]:
        raise NotImplementedError

    def get_detectors(self) -> List[AbstractDetector]:
        raise NotImplementedError


class AbstractMeasurement:
    """
    Abstract class to be inherited by any measurement implemented on the server side.
    """

    def __init__(self):
        """
        Constructor for the Measurement class.
        """
        self.is_busy = False

    def start(self):
        raise NotImplementedError

    def abort(self):
        raise NotImplementedError

    def get_result(self):
        raise NotImplementedError
