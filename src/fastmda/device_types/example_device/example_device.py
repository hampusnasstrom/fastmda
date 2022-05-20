import asyncio
from typing import List, Dict, Union, Tuple, Mapping

from fastmda import schemas
from fastmda.exceptions import FastMDAConnectFailed
from fastmda.objects import AbstractDevice, DiscreteActuator, ContinuousActuator, Detector, DiscreteSetting, \
    ContinuousSetting
from fastmda.schemas import DeviceType


class MyActuator(DiscreteActuator):

    def __init__(self, actuator_id, parent):
        super().__init__(actuator_id=actuator_id, parent=parent)
        self._position = 0
        self._position_values = ["off", "on"]
        self._unit = schemas.Unit()
        self._settings = {1: DelaySetting(1, self)}

    @property
    def name(self) -> str:
        return f"My actuator number {self.actuator_id}"

    @property
    def settings(self) -> Mapping[int, Union[DiscreteSetting, ContinuousSetting]]:
        return self._settings

    async def get_value(self) -> str:
        await asyncio.sleep(0.01)
        return self._position_values[self._position]

    def get_value_options(self) -> List[str]:
        return self._position_values

    async def _set_value(self, value_index: int):
        self._position = value_index
        wait_time = await self._settings[1].get_value()
        await asyncio.sleep(wait_time)

    @property
    def unit(self) -> schemas.Unit:
        return self._unit

    def is_able_to_set(self) -> bool:
        return True


class Device(AbstractDevice):

    @staticmethod
    def device_type():
        return DeviceType(name="Example device",
                          device_description="An example of how to implement a device",
                          args={
                              "com_port": "COM port on which the device is located (as an example)"
                          })

    def __init__(self, device_id: int, com_port: str):
        self.com_port = com_port
        self._is_connected = False
        super().__init__(device_id=device_id)
        self._actuators = {1: MyActuator(1, self)}

    @property
    def detectors(self) -> Dict[int, Detector]:
        return {}

    @property
    def actuators(self) -> Mapping[int, Union[DiscreteActuator, ContinuousActuator]]:
        return self._actuators

    @property
    def settings(self) -> Dict[int, Union[DiscreteSetting, ContinuousSetting]]:
        return {}

    def connect(self) -> bool:
        if self.com_port == "COM1":
            self._is_connected = True
            return self._is_connected
        else:
            raise FastMDAConnectFailed(self.device_type(), self.device_id, f"{self.com_port}, invalid com port.")

    def disconnect(self) -> bool:
        if self._is_connected:
            self._is_connected = False
        return True

    def is_connected(self) -> bool:
        return self._is_connected


class DelaySetting(ContinuousSetting):

    def __init__(self, setting_id: int, parent: Union[AbstractDevice, DiscreteActuator, ContinuousActuator, Detector]):
        super().__init__(setting_id, parent)
        self._hard_limits = (0., 1e3)
        self._wait_time = 0.
        self._name = "Set wait time"
        self._unit = schemas.Unit(str_rep="Seconds", si_base="s")

    def get_hard_limits(self) -> Tuple[float, float]:
        return self._hard_limits

    async def get_value(self) -> float:
        return self._wait_time

    async def _set_value(self, value: float):
        self._wait_time = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def unit(self) -> schemas.Unit:
        return self._unit

    def is_able_to_set(self) -> bool:
        return True
