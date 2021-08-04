from typing import List
from object_examples import Device, Controller, Detector


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

    def get_controllers(self) -> List[Controller]:
        pass

    def get_detectors(self) -> List[Detector]:
        return []
