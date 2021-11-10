from types import ModuleType
from typing import Dict, Optional, Any

from pydantic import BaseModel, Field


class DeviceInfoBase(BaseModel):
    device_type: str = Field(...,
                             description="The type of device, corresponds to the python script where the Device " +
                                         "class is defined without the .py extension.")
    name: str = Field(..., description="A user readable name for the device, should be unique.")
    args: Dict[str, Any] = Field(..., description="A dict of arguments needed to initialize the Device object.")


class DeviceInfoCreate(DeviceInfoBase):
    pass


class DeviceInfo(DeviceInfoBase):
    id: int
    is_connected: Optional[bool] = False

    class Config:
        orm_mode = True


class DeviceType(BaseModel):
    name: str = Field(None, description="Name of the device type.")
    device_description: Optional[str] = Field(None, description="Description of the device type.")
    args: Dict[str, str] = Field(None, description="Dict of arguments needed to construct the device.")


class ActuatorInfo(BaseModel):
    name: str = Field(None, description="Name of the actuator")
    major_axis: bool = Field(True, description="Major axis or not")


class Unit(BaseModel):
    str_repr: str = Field("", description="A string representation of the unit.")
    si_base: str = Field("", description="The SI base unit.")
    si_prefix_factor: float = Field(1.0, description="The factor by which the SI unit is scaled.")
    si_prefix_str: Optional[str] = Field(None, description="The prefix of the SI unit.")
