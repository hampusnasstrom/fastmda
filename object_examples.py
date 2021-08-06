from typing import List
from dataclasses import dataclass


class Detector:

    def __init__(self, dimensionality: int = 1):
        self.dimensionality = dimensionality

    def acquire(self):
        raise NotImplementedError


@dataclass
class ActuatorType:
    type: str
    long_name: str


class Actuator:

    def __init__(self):
        self.position = 0

    def get_position(self):
        raise NotImplementedError

    def get_actuator_type(self) -> ActuatorType:
        raise NotImplementedError


class Device:

    def __init__(self, device_id: str):
        self.id = device_id

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def get_actuators(self) -> List[Actuator]:
        raise NotImplementedError

    def get_detectors(self) -> List[Detector]:
        raise NotImplementedError
