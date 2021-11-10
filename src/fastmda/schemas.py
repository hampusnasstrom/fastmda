from types import ModuleType
from typing import Dict, Optional, Any

from pydantic import BaseModel, Field


class DeviceInfoBase(BaseModel):
    device_type: str = Field(...,
                             description="The type of device, corresponds to the python script where the Device " +
                                         "class is defined without the .py extension.")
    name: str = Field(..., description="A user readable name for the device, should be unique.")
    args: Dict[str, Any]


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
