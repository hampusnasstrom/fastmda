from typing import Dict, Optional, Any, List, Tuple, Union

from pydantic import BaseModel, Field


# Devices:

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
    name: str = Field(..., description="Name of the device type.")
    device_description: Optional[str] = Field(..., description="Description of the device type.")
    args: Dict[str, str] = Field(..., description="Dict of arguments needed to construct the device.")


# Actuators:

class ActuatorInfo(BaseModel):
    name: str = Field(..., description="Name of the actuator to display to user.")
    actuator_id: int = Field(..., description="Unique id of the actuator.")
    device_id: int = Field(..., description="Unique id of the parent device.")


class DiscreteActuatorInfo(ActuatorInfo):
    # value: str = Field(..., description="Current position of the actuator.")
    options: List[str] = Field(..., description="A list of all the possible values.")
    invalid_values: List[int] = Field([], description="A list of all the options which have been software disabled.")


class ContinuousActuatorInfo(ActuatorInfo):
    # value: float = Field(..., description="Current position of the actuator.")
    hardware_limits: Tuple[Union[float, None], Union[float, None]] = Field(
        (None, None),
        description="A tuple of the (lower, upper) hardware limits of the actuator."
    )
    software_limits: Tuple[Union[float, None], Union[float, None]] = Field(
        (None, None),
        description="A tuple of the (lower, upper) software limits of the actuator."
    )


# Detector:

class DetectorInfo(BaseModel):
    name: str = Field(..., description="Name of the detector to display to the user.")
    detector_id: int = Field(..., description="Unique (for the device) ID of the detector.")
    device_id: int = Field(..., description="Unique ID of the parent device.")
    dimensionality: int = Field(..., description="Dimensionality of the detector.")


# Settings:

class SettingInfo(BaseModel):
    name: str = Field(..., description="Name of the actuator to display to user.")
    setting_id: int = Field(..., description="Unique (for the parent) ID of the setting.")
    parent_id: int = Field(..., description="Unique ID of the parent device.")
    grandparent_id: int = Field(None, description="If the parent device is an actuator or detector, this is the" + \
                                                  "unique ID of their parent device, otherwise None.")


class DiscreteSettingInfo(SettingInfo):
    # value: str = Field(..., description="Current value of the setting.")
    options: List[str] = Field(..., description="A list of all the possible values.")
    invalid_values: List[int] = Field([], description="A list of all the options which have been software disabled.")


class ContinuousSettingInfo(SettingInfo):
    # value: float = Field(..., description="Current value of the setting.")
    hard_limits: Tuple[Union[float, None], Union[float, None]] = Field(
        (None, None),
        description="A tuple of the (lower, upper) hard limits of the setting."
    )
    soft_limits: Tuple[Union[float, None], Union[float, None]] = Field(
        (None, None),
        description="A tuple of the (lower, upper) soft limits of the setting."
    )


# Response:

class Detail(BaseModel):
    detail: str


# Additional:

class Unit(BaseModel):
    str_repr: str = Field("", description="A string representation of the unit.")
    si_base: str = Field("", description="The SI base unit.")
    si_prefix_factor: float = Field(1.0, description="The factor by which the SI unit is scaled.")
    si_prefix_str: Optional[str] = Field(None, description="The prefix of the SI unit.")
