from typing import List, Dict

from fastmda.exceptions import FastMDAConnectFailed
from fastmda.objects import AbstractDevice, DeviceObjects
from fastmda.schemas import DeviceType


class Device(AbstractDevice):
    device_type = DeviceType(name="Example device",
                             device_description="An example of how to implement a device",
                             args={
                                 "com_port": "COM port on which the device is located (as an example)"
                             })

    def __init__(self, com_port: str):
        self.com_port = com_port
        self._is_connected = False
        super().__init__()
        self.objects = DeviceObjects()

    def connect(self) -> bool:
        if self.com_port == "COM1":
            self._is_connected = True
            return self._is_connected
        else:
            raise FastMDAConnectFailed(self.device_type, f"{self.com_port}, invalid com port.")

    def disconnect(self) -> bool:
        if self._is_connected:
            self._is_connected = False
        return True

    def is_connected(self) -> bool:
        return self._is_connected
