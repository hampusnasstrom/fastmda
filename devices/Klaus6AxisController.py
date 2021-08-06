from typing import List
from object_examples import Device, Actuator, Detector


class Klaus6AxisController(Device):

    def __init__(self, com_port: str):
        self.com_port = com_port
        self.connect()
        super().__init__(self.get_id())

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_id(self) -> str:
        return f'{self.com_port}_6AxisController'

    def get_actuators(self) -> List[Actuator]:
        pass

    def get_detectors(self) -> List[Detector]:
        return []


if __name__ == "__main__":
    # Testing:
    device_instance = Klaus6AxisController('COM1')
    print(device_instance.id)
    print(device_instance.get_detectors())
