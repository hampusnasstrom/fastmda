from types import ModuleType
from typing import Dict

from fastmda.objects import AbstractDevice
from fastmda.schemas import DeviceType

device_dict: Dict[int, AbstractDevice] = {}
device_types_info: Dict[str, DeviceType] = {}
device_types_modules: Dict[str, ModuleType] = {}
