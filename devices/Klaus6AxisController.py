from typing import List

from FastMDAExceptions import FastMDAConnectFailed
from object_examples import Device, Actuator, Detector


class Klaus6AxisController(Device):

    def __init__(self, com_port: str):
        self.com_port = com_port
        super().__init__(self.get_id())

    def connect(self) -> bool:
        raise FastMDAConnectFailed(self, "Connect method not implemented.")

    def disconnect(self) -> bool:
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError

    def get_id(self) -> str:
        return f'{self.com_port}_6AxisController'

    def get_actuators(self) -> List[Actuator]:
        raise NotImplementedError

    def get_detectors(self) -> List[Detector]:
        return []


if __name__ == "__main__":
    # Testing:
    device_instance = Klaus6AxisController('COM1')
    print(device_instance.id)
    print(device_instance.get_detectors())
    try:
        device_instance.connect()
    except FastMDAConnectFailed as e:
        print(e)