from typing import List
from object_examples import Device, Actuator, Detector


class Klaus6AxisController(Device):

    def __init__(self, com_port: str):
        self.com_port = com_port
        self.connect()
        super(Klaus6AxisController).__init__(self.get_id())

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_id(self) -> str:
        pass

    def get_actuators(self) -> List[Actuator]:
        pass

    def get_detectors(self) -> List[Detector]:
        return []
