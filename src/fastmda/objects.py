from typing import List, Dict, Tuple, Union

from pydantic import BaseModel, Field

from fastmda import schemas
from fastmda.exceptions import FastMDAatSoftwareLimit


class Detector:
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


class Actuator:
    """
    Abstract class for the actuator part of the device.
    """
    actuator_info: schemas.ActuatorInfo()  # Should be overwritten by implementing class

    def __init__(self):
        """
        Constructor of the Actuator class.
        """


class DiscreteActuator(Actuator):
    """
    Abstract class for a discrete actuator.
    """

    def __init__(self):
        """
        Constructor of the DiscreteActuator class.
        """
        super().__init__()
        self._invalid_positions = []
        self._units = schemas.Unit()

    def get_position_values(self) -> List[str]:
        """
        Get a list of all the options as strings, should be overridden in subclass.

        :return: list of all the options as strings.
        :rtype: List[str]
        """
        raise NotImplementedError

    def get_position(self) -> int:
        """
        Get the index of the current position, should be overridden in subclass.

        :return: Index of current position.
        :rtype: int
        """
        raise NotImplementedError

    def _set_position(self, position_index: int):
        """
        Private method for setting the position of the actuator, should be overridden in subclass.

        :param position_index: Index of the position to set.
        :type position_index: int
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def get_units(self) -> schemas.Unit:
        """
        Method for getting the units of the positions (if any).

        :return: The units
        :rtype: fastmda.schemas.Unit
        """
        return self._units

    def get_position_value(self) -> str:
        """
        Convenience method for getting the string value of the current position.

        :return: The string value of the current position.
        :rtype: str
        """
        return self.get_position_values()[self.get_position()]

    def set_invalid_positions(self, invalid_position: int):
        """
        Method for setting temporarily invalid positions.

        :param invalid_position: The index of the invalid position.
        :type invalid_position: int
        :return: None
        :rtype: None
        """
        if invalid_position not in self._invalid_positions:
            self._invalid_positions.append(invalid_position)

    def set_valid_positions(self, valid_position: int):
        """
        Method for setting temporarily invalid position to be valid again.

        :param valid_position: The index of the valid position.
        :type valid_position: int
        :return: None
        :rtype: None
        """
        if valid_position not in self._invalid_positions:
            self._invalid_positions.remove(valid_position)

    def set_position(self, position_index: int):
        """
        Method for setting the position of the actuator.

        :param position_index: Index of the position to set.
        :type position_index: int
        :return: None
        :rtype: None
        :raises FastMDAatSoftwareLimit: If position is temporarily set as invalid.
        """
        if position_index in self._invalid_positions:
            raise FastMDAatSoftwareLimit(self.actuator_info)
        else:
            self._set_position(position_index)


class ContinuousActuator(Actuator):
    """
    Abstract class for a continuous actuator.
    """

    def __init__(self):
        """
        Constructor of the ContinuousActuator class.
        """
        super().__init__()
        self._software_limits = (-float("inf"), float("inf"))
        self._units = schemas.Unit()

    def get_position(self) -> float:
        """
        Method for getting the position of the actuator, should be overridden in subclass.

        :return: The position of the actuator.
        :rtype: float
        """
        raise NotImplementedError

    def get_hardware_limits(self) -> Tuple[float, float]:
        """
        Method for getting the hardware limits of the actuator, should be overridden in subclass.

        :return: A tuple of the (lower, upper) limit of the actuator.
        :rtype: Tuple[float, float]
        """
        raise NotImplementedError

    def _set_position(self, position: float):
        """
        Private method for setting the position of the actuator, should be overridden in subclass.

        :param position: Position to set the actuator to.
        :type position: float
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def get_units(self) -> schemas.Unit:
        """
        Method for getting the units of the position (if any).

        :return: The units of the position.
        :rtype: fastmda.schemas.Unit
        """
        return self._units

    def get_software_limits(self) -> Tuple[float, float]:
        """
        Method for getting the software limits of the actuator.

        :return: A tuple of the (lower, upper) limit of the actuator.
        :rtype: Tuple[float, float]
        """
        return self._software_limits

    def set_software_limits(self, limits: Tuple[float, float]):
        """
        Method for setting the software limits of the actuator.

        :param limits: A tuple of the (lower, upper) limit of the actuator. Use (+ or -) float("inf") for no limit.
        :type limits: Tuple[float, float]
        :return: None
        :rtype: None
        """
        self._software_limits = limits

    def set_position(self, position: float):
        """
        Method for setting the position of the actuator.

        :param position: Position to set the actuator to.
        :type position: float
        :return: None
        :rtype: None
        """
        if self._software_limits[0] < position < self._software_limits[1]:
            self._set_position(position)


class DeviceObjects(BaseModel):
    actuators: Dict[int, Actuator] = Field({}, description="Dictionary of actuator objects")
    detectors: Dict[int, Detector] = Field({}, description="Dictionary of detector objects")

    class Config:
        arbitrary_types_allowed = True


class AbstractDevice:
    """
    Abstract class to be inherited by any device the controls the communication with actuators and/or detectors.
    """
    device_type = schemas.DeviceType()  # Should be overridden in subclass

    def __init__(self):
        """
        Constructor of the Device class.
        """
        self.objects = DeviceObjects()

    def connect(self) -> bool:
        raise NotImplementedError

    def disconnect(self) -> bool:
        raise NotImplementedError

    def is_connected(self) -> bool:
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
