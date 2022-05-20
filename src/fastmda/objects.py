from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Mapping

from xarray import DataArray, Dataset

from fastmda import schemas
from fastmda.exceptions import FastMDAatSoftwareLimit, FastMDAatHardwareLimit, FastMDAatSoftSettingLimit, \
    FastMDAatHardSettingLimit, FastMDAisBusy


def within_limit(value: float, limits: Tuple[Union[float, None], Union[float, None]]) -> bool:
    """
    Help function for checking if value is within limits where None corresponds to no limit.

    :param value: The value to check if it is within the limit.
    :type value: float
    :param limits: A tuple of the (lower, upper) limit of the value, None means no limit.
    :type limits: Tuple[Union[float, None], Union[float, None]]
    :return: If the value is within the limits or not.
    :rtype: bool
    """
    return (
            (limits[0] is None or limits[0] <= value)
            and
            (limits[1] is None or value <= limits[1])
    )


class __Value(ABC):
    """
    Hidden base class for value.
    """

    def __init__(self):
        """
        Init method for __Value class.
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Abstract property getter method for the name of the value.

        :return: The name of the value instance
        :rtype: str
        """

    @property
    @abstractmethod
    def unit(self) -> schemas.Unit:
        """
        Abstract property getter method for the unit of the value.

        :return: The unit of the value.
        :rtype: fastmda.schemas.Unit
        """

    @abstractmethod
    def is_able_to_set(self) -> bool:
        """
        Method for checking whether the value can be set.

        :return: Whether or not the value can be set.
        :rtype: bool
        """


class __DiscreteValue(__Value, ABC):
    """
    Hidden base class for discrete value.
    """

    def __init__(self):
        """
        Init method for __DiscreteValue class.
        """
        super().__init__()
        self._invalid_value_index = []

    @abstractmethod
    async def get_value(self) -> str:
        """
        Asynchronous method for getting the current value as a string.

        :return: The current value as a string.
        :rtype: str
        """

    @abstractmethod
    def get_value_options(self) -> List[str]:
        """
        Method for getting a list of all optional values.

        :return:
        :rtype:
        """

    @abstractmethod
    async def _set_value(self, value_index: int):
        """
        Asynchronous private method for setting the current value by the zero indexed position in the value options
        list.

        :param value_index: The index of the value to set.
        :type value_index: int
        :return: None
        :rtype: None
        """

    def set_invalid_value(self, invalid_value_index: int):
        """
        Method for setting temporarily invalid values.

        :param invalid_value_index: The index of the invalid values.
        :type invalid_value_index: int
        :return: None
        :rtype: None
        """
        if invalid_value_index not in self._invalid_value_index:
            self._invalid_value_index.append(invalid_value_index)

    def get_invalid_values(self) -> List[int]:
        """
        Method for getting temporarily invalid value index.

        :return: A list of the index of the temporarily invalid values.
        :rtype: List[int]
        """
        return self._invalid_value_index

    def set_valid_value(self, valid_value_index: int):
        """
        Method for setting temporarily invalid values to be valid again.

        :param valid_value_index: The index of the valid value.
        :type valid_value_index: int
        :return: None
        :rtype: None
        """
        if valid_value_index not in self._invalid_value_index:
            self._invalid_value_index.remove(valid_value_index)


class __ContinuousValue(__Value, ABC):
    """
    Hidden base class for a continuous value.
    """

    def __init__(self):
        """
        Init method for __ContinuousValue class.
        """
        super().__init__()
        self._soft_limits: Tuple[Union[float, None], Union[float, None]] = (None, None)

    @abstractmethod
    def get_hard_limits(self) -> Tuple[Union[float, None], Union[float, None]]:
        """
        Method for getting the hard limits of the value, should be overridden in subclass.

        :return: A tuple of the (lower, upper) limit of the actuator.
        :rtype: Tuple[Union[float, None], Union[float, None]]
        """

    @abstractmethod
    async def get_value(self) -> float:
        """
        Asynchronous method for getting the current value, should be overridden in subclass.

        :return: The current value.
        :rtype: float
        """

    @abstractmethod
    async def _set_value(self, value: float):
        """
        Asynchronous private method for setting the value of the actuator, should be overridden in subclass.

        :param value: Value to set the actuator to.
        :type value: float
        :return: None
        :rtype: None
        """

    def get_soft_limits(self) -> Tuple[Union[float, None], Union[float, None]]:
        """
        Method for getting the software limits of the actuator.

        :return: A tuple of the (lower, upper) limit of the actuator.
        :rtype: Tuple[Union[float, None], Union[float, None]]
        """
        return self._soft_limits

    def set_soft_limits(self, limits: Tuple[Union[float, None], Union[float, None]]):
        """
        Method for setting the soft limits of the value.

        :param limits: A tuple of the (lower, upper) limit of the value. Use None for no limit.
        :type limits: Tuple[Union[float, None], Union[float, None]]
        :return: None
        :rtype: None
        """
        self._soft_limits = limits


class DiscreteSetting(__DiscreteValue, ABC):
    """
    Abstract class for a discrete setting.
    """

    def __init__(self, setting_id: int, parent: Union[AbstractDevice, DiscreteActuator, ContinuousActuator, Detector]):
        """
        Constructor of the DiscreteSetting class.

        :param setting_id: The unique ID of the setting.
        :type setting_id: int
        :param parent: The parent device of the setting.
        :type parent: Union[AbstractDevice, DiscreteActuator, ContinuousActuator, Detector]
        """
        super().__init__()
        self.setting_id = setting_id
        self.parent = parent

    async def set_value(self, value_index: int):
        """
        Asynchronous method for setting the value of the setting.

        :param value_index: Index of the value to set.
        :type value_index: int
        :return: None
        :rtype: None
        :raises FastMDAatSoftSettingLimit: If value is temporarily set as invalid.
        :raises FastMDAatHardSettingLimit: If index is out of bounds.
        :raises FastMDAisBusy: If the device is busy.
        """
        if not self.is_able_to_set():
            if isinstance(self.parent, AbstractDevice):
                device_id = self.parent.device_id
            else:
                device_id = self.parent.parent.device_id
            raise FastMDAisBusy(device_id)
        if value_index >= len(self.get_value_options()):
            raise FastMDAatHardSettingLimit(setting_info=self.info)
        if value_index in self._invalid_value_index:
            raise FastMDAatSoftSettingLimit(setting_info=self.info)
        else:
            await self._set_value(value_index)

    @property
    def info(self) -> schemas.DiscreteSettingInfo:
        """
        Getter method for the info property.

        :return: The info for the instance of the discrete setting.
        :rtype: schemas.DiscreteSettingInfo
        :raises ValueError: If parent property is not of known type.
        """
        if isinstance(self.parent, AbstractDevice):
            parent_id = self.parent.device_id
            grandparent_id = None
        elif isinstance(self.parent, DiscreteActuator) or isinstance(self.parent, ContinuousActuator):
            parent_id = self.parent.actuator_id
            grandparent_id = self.parent.parent.device_id
        elif isinstance(self.parent, Detector):
            parent_id = self.parent.detector_id
            grandparent_id = self.parent.parent.device_id
        else:
            raise ValueError("parent is not of known type.")
        return schemas.DiscreteSettingInfo(
            name=self.name,
            setting_id=self.setting_id,
            parent_id=parent_id,
            grandparent_id=grandparent_id,
            # value=self.get_value(),
            options=self.get_value_options(),
            invalid_values=self.get_invalid_values()
        )


class ContinuousSetting(__ContinuousValue, ABC):
    """
    Abstract class for a continuous setting.
    """

    def __init__(self, setting_id: int, parent: Union[AbstractDevice, DiscreteActuator, ContinuousActuator, Detector]):
        """
        Constructor of the ContinuousSetting class.

        :param setting_id: The unique ID of the setting.
        :type setting_id: int
        :param parent: The parent device of the setting.
        :type parent: Union[AbstractDevice, DiscreteActuator, ContinuousActuator, Detector]
        """
        super().__init__()
        self.setting_id = setting_id
        self.parent = parent

    async def set_value(self, value: float):
        """
        Asynchronous method for setting the value of the setting.

        :param value: Value to set the setting to.
        :type value: float
        :return: None
        :rtype: None
        :raises FastMDAatSoftwareLimit: If value is outside soft limits.
        :raises FastMDAatHardwareLimit: If value is outside hard limits.
        :raises FastMDAisBusy: If the device is busy.
        """
        if not self.is_able_to_set():
            if isinstance(self.parent, AbstractDevice):
                device_id = self.parent.device_id
            else:
                device_id = self.parent.parent.device_id
            raise FastMDAisBusy(device_id)
        hard_limits = self.get_hard_limits()
        if not within_limit(value, hard_limits):
            raise FastMDAatHardSettingLimit(setting_info=self.info)
        if within_limit(value, self._soft_limits):
            await self._set_value(value)
        else:
            raise FastMDAatSoftSettingLimit(setting_info=self.info)

    @property
    def info(self) -> schemas.ContinuousSettingInfo:
        """
        Getter method for the info property.

        :return: The info for the instance of the continuous setting.
        :rtype: schemas.ContinuousSettingInfo
        :raises ValueError: If parent property is not of known type.
        """
        if isinstance(self.parent, AbstractDevice):
            parent_id = self.parent.device_id
            grandparent_id = None
        elif isinstance(self.parent, DiscreteActuator) or isinstance(self.parent, ContinuousActuator):
            parent_id = self.parent.actuator_id
            grandparent_id = self.parent.parent.device_id
        elif isinstance(self.parent, Detector):
            parent_id = self.parent.detector_id
            grandparent_id = self.parent.parent.device_id
        else:
            raise ValueError("parent is not of known type.")
        return schemas.ContinuousSettingInfo(
            name=self.name,
            setting_id=self.setting_id,
            parent_id=parent_id,
            grandparent_id=grandparent_id,
            # value=self.get_value(),
            hard_limits=self.get_hard_limits(),
            soft_limits=self._soft_limits
        )


class DiscreteActuator(__DiscreteValue, ABC):
    """
    Abstract class for a discrete actuator.
    """

    def __init__(self, actuator_id: int, parent: AbstractDevice):
        """
        Constructor of the DiscreteActuator class.

        :param actuator_id: The unique ID of the actuator.
        :type actuator_id: int
        :param parent: The parent device of the actuator.
        :type parent: AbstractDevice
        """
        super().__init__()
        self.actuator_id = actuator_id
        self.parent = parent

    @property
    @abstractmethod
    def settings(self) -> Mapping[int, Union[DiscreteSetting, ContinuousSetting]]:
        """
        Getter method for the settings property. Should return a dict with integer keys and setting object values.

        :return: A dictionary of all the settings.
        :rtype: Mapping[int, Union[DiscreteSetting, ContinuousSetting]]
        """

    async def set_value(self, value_index: int):
        """
        Asynchronous method for setting the value.

        :param value_index: Index of the value to set.
        :type value_index: int
        :return: None
        :rtype: None
        :raises FastMDAatSoftwareLimit: If value is temporarily set as invalid.
        :raises FastMDAatHardwareLimit: If index is out of bounds.
        :raises FastMDAisBusy: If the device is busy.
        """
        if not self.is_able_to_set():
            raise FastMDAisBusy(self.parent.device_id)
        if value_index >= len(self.get_value_options()):
            raise FastMDAatHardwareLimit(actuator_info=self.info)
        if value_index in self._invalid_value_index:
            raise FastMDAatSoftwareLimit(actuator_info=self.info)
        else:
            await self._set_value(value_index)

    @property
    def info(self) -> schemas.DiscreteActuatorInfo:
        """
        Getter method for the info property.

        :return: The info for the instance of the discrete actuator.
        :rtype: schemas.DiscreteActuatorInfo
        """
        return schemas.DiscreteActuatorInfo(
            name=self.name,
            actuator_id=self.actuator_id,
            device_id=self.parent.device_id,
            # value=self.get_value(),
            options=self.get_value_options(),
            invalid_values=self.get_invalid_values()
        )


class ContinuousActuator(__ContinuousValue, ABC):
    """
    Abstract class for a continuous actuator.
    """

    def __init__(self, actuator_id: int, parent: AbstractDevice):
        """
        Constructor of the ContinuousActuator class.

        :param actuator_id: The unique ID of the actuator.
        :type actuator_id: int
        :param parent: The parent device of the actuator.
        :type parent: AbstractDevice
        """
        super().__init__()
        self.actuator_id = actuator_id
        self.parent = parent

    @property
    @abstractmethod
    def settings(self) -> Mapping[int, Union[DiscreteSetting, ContinuousSetting]]:
        """
        Getter method for the settings property. Should return a dict with integer keys and setting object values.

        :return: A dictionary of all the settings.
        :rtype: Mapping[int, Union[DiscreteSetting, ContinuousSetting]]
        """

    async def set_value(self, value: float):
        """
        Asynchronous method for setting the value of the actuator.

        :param value: Value to set the actuator to.
        :type value: float
        :return: None
        :rtype: None
        :raises FastMDAatSoftwareLimit: If value is outside software limits.
        :raises FastMDAatHardwareLimit: If value is outside hardware limits.
        :raises FastMDAisBusy: If the device is busy.
        """
        if not self.is_able_to_set():
            raise FastMDAisBusy(self.parent.device_id)
        hard_limits = self.get_hard_limits()
        if not within_limit(value, hard_limits):
            raise FastMDAatHardwareLimit(actuator_info=self.info)
        if within_limit(value, self._soft_limits):
            await self._set_value(value)
        else:
            raise FastMDAatSoftwareLimit(actuator_info=self.info)

    @property
    def info(self) -> schemas.ContinuousActuatorInfo:
        """
        Getter method for the info property.

        :return: The info for the instance of the discrete actuator.
        :rtype: schemas.DiscreteActuatorInfo
        """
        return schemas.ContinuousActuatorInfo(
            name=self.name,
            actuator_id=self.actuator_id,
            device_id=self.parent.device_id,
            # value=self.get_value(),
            hardware_limits=self.get_hard_limits(),
            software_limits=self._soft_limits
        )


class Detector(ABC):
    """
    Abstract class for the detector part of the device.
    """

    def __init__(self, detector_id: int, parent: AbstractDevice, dimensionality: int = 1):
        """
        Constructor for the super class

        :param detector_id: The unique ID of the detector
        :type detector_id: int
        :param parent: The parent device of the detector
        :type parent: AbstractDevice
        :param dimensionality: The dimensionality of the detector, i.e. the dimension of the output array.
        :type dimensionality: int
        """
        self.detector_id = detector_id
        self.parent = parent
        self.dimensionality = dimensionality

    @property
    @abstractmethod
    def settings(self) -> Mapping[int, Union[DiscreteSetting, ContinuousSetting]]:
        """
        Getter method for the settings property. Should return a dict with integer keys and setting object values.

        :return: A dictionary of all the settings.
        :rtype: Mapping[int, Union[DiscreteSetting, ContinuousSetting]]
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Abstract property getter method for the name of the detector.

        :return: The name of the detector instance
        :rtype: str
        """

    @abstractmethod
    def is_able_to_acquire(self) -> bool:
        """
        Method for checking whether the detector is available for acquiring.

        :return: Whether or not the detector can acquire.
        :rtype: bool
        """

    @abstractmethod
    def _acquire(self) -> DataArray:
        """
        Method for acquiring data from the detector, should return a DataArray with a name, attributes long_name and
        units as well as labeled dimension arrays (if dimension > 0).

        :return: The measured data in a DataArray
        :rtype: xarray.DataArray
        """

    def acquire(self) -> DataArray:
        """
        Method for acquiring data from the detector, returns a DataArray with a name, attributes long_name and
        units as well as labeled dimension arrays (if dimension > 0).

        :return: The measured data in a DataArray
        :rtype: xarray.DataArray
        """
        if self.is_able_to_acquire():
            return self._acquire()
        else:
            raise FastMDAisBusy(self.parent.device_id)

    @property
    def info(self):
        """
        Getter method for the info property.

        :return: The info for the instance of the detector.
        :rtype: schemas.DetectorInfo
        """
        return schemas.DetectorInfo(
            name=self.name,
            actuator_id=self.detector_id,
            device_id=self.parent.device_id,
            dimensionality=self.dimensionality
        )


class AbstractDevice(ABC):
    """
    Abstract class to be inherited by any device the controls the communication with actuators and/or detectors.
    """

    @staticmethod
    @abstractmethod
    def device_type() -> schemas.DeviceType:
        pass

    def __init__(self, device_id: int):
        """
        Constructor of the Device class.

        :param device_id: The unique ID of the device.
        :type device_id: int
        """
        self.device_id = device_id

    @property
    @abstractmethod
    def actuators(self) -> Mapping[int, Union[DiscreteActuator, ContinuousActuator]]:
        """
        Getter method for the actuators property. Should return a dict with integer keys and actuator object values.

        :return: A dictionary of all the actuators.
        :rtype: Mapping[int, Union[DiscreteActuator, ContinuousActuator]]
        """

    @property
    @abstractmethod
    def detectors(self) -> Mapping[int, Detector]:
        """
        Getter method for the detectors property. Should return a dict with integer keys and detector object values.

        :return: A dictionary of all the detectors.
        :rtype: Mapping[int, Detector]
        """

    @property
    @abstractmethod
    def settings(self) -> Mapping[int, Union[DiscreteSetting, ContinuousSetting]]:
        """
        Getter method for the settings property. Should return a dict with integer keys and setting object values.

        :return: A dictionary of all the settings.
        :rtype: Mapping[int, Union[DiscreteSetting, ContinuousSetting]]
        """

    @abstractmethod
    def connect(self) -> bool:
        """
        Method for connecting to the device. Should return True when the device is connected, otherwise a
        fastmda.exceptions.FastMDAConnectFailed error should be raised.

        :return: The success of the connection.
        :rtype: bool
        """

    @abstractmethod
    def disconnect(self) -> bool:
        """
        Method for connecting to the device. Should return True when the device is disconnected, otherwise a
        fastmda.exceptions.FastMDADisconnectFailed error should be raised.

        :return: The success of the disconnection. I.e. True when the device is disconnected.
        :rtype: bool
        """

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Method for getting whether the device is connected or not.

        :return: Whether the device is connected or not.
        :rtype: bool
        """


class AbstractMeasurement(ABC):
    """
    Abstract class to be inherited by any measurement implemented on the server side.
    """

    def __init__(self):
        """
        Constructor for the Measurement class.
        """

    @abstractmethod
    def start(self):
        """
        Method for starting the measurement.

        :return: None
        :rtype: None
        """

    @abstractmethod
    def abort(self):
        """
        Method for aborting the measurement.

        :return: None
        :rtype: None
        """

    @abstractmethod
    def get_result(self) -> Dataset:
        """
        Method for getting the Dataset with the current measurement data.

        :return: The measurement data recorded so far.
        :rtype: xarray.Dataset
        """
