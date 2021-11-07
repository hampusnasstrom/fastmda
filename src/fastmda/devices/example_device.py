from typing import List

from fastmda.exceptions import FastMDAConnectFailed
from fastmda.objects import AbstractDevice, AbstractActuator, AbstractDetector


class Device(AbstractDevice):

    def __init__(self, com_port: str):
        self.com_port = com_port
        super().__init__(self.get_id())

    def connect(self) -> bool:
        if self.com_port == "COM1":
            return True
        else:
            raise FastMDAConnectFailed(self, f"{self.com_port}, invalid com port.")

    def disconnect(self) -> bool:
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError

    def get_id(self) -> str:
        return f'{self.com_port}_example_device'

    def get_actuators(self) -> List[AbstractActuator]:
        raise NotImplementedError

    def get_detectors(self) -> List[AbstractDetector]:
        return []
