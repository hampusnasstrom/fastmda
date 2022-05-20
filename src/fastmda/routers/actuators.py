import asyncio
from typing import List, Union

from fastapi import APIRouter, Path, HTTPException, status, Query

from fastmda import schemas
from fastmda.database import SessionLocal
from fastmda.exceptions import FastMDAisBusy, FastMDAatHardSettingLimit, FastMDAatSoftSettingLimit
from fastmda.globals import device_dict
from fastmda.objects import DiscreteActuator, ContinuousActuator

router = APIRouter(
    prefix="/devices/{device_id}/actuators",
    tags=["actuators"]
)
responses = {
    status.HTTP_404_NOT_FOUND: {
        "model": schemas.Detail,
        "description": "Device, actuator and/or setting with given ID not found."
    },
    status.HTTP_504_GATEWAY_TIMEOUT: {
        "model": schemas.Detail,
        "description": "The set or get of a value could not be performed within the set timeout."
    },
    status.HTTP_406_NOT_ACCEPTABLE: {
        "model": schemas.Detail,
        "description": "The value to set was not accepted."
    },
    status.HTTP_423_LOCKED: {
        "model": schemas.Detail,
        "description": "The device is busy."
    }
}
set_timeout = 5
get_timeout = 0.1


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/discrete", response_model=List[schemas.DiscreteActuatorInfo], summary="Get all discrete actuators",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device with given ID not found."
                }
            })
async def get_all_discrete_actuators(device_id: int = Path(..., description="The ID of the device.")):
    """
    Get a list of information for all discrete actuators of the specified device.
    """
    try:
        return [act.info for _, act in device_dict[device_id].actuators.items() if isinstance(act, DiscreteActuator)]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")


@router.get("/continuous", response_model=List[schemas.ContinuousActuatorInfo], summary="Get all continuous actuators",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device with given ID not found."
                }
            })
async def get_all_continuous_actuators(device_id: int = Path(..., description="The ID of the device.")):
    """
    Get a list of information for all continuous actuators of the specified device.
    """
    try:
        return [act.info for _, act in device_dict[device_id].actuators.items() if isinstance(act, ContinuousActuator)]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")


@router.get("/{actuator_id}", response_model=Union[schemas.DiscreteActuatorInfo, schemas.ContinuousActuatorInfo],
            summary="Get actuator information",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device and/or actuator with given ID not found."
                }
            })
async def get_actuator(device_id: int = Path(..., description="The ID of the device."),
                       actuator_id: int = Path(..., description="The ID of the actuator.")):
    """
    Get the information for the specified actuator of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return device.actuators[actuator_id].info
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")


@router.get("/{actuator_id}/value", response_model=Union[str, float], summary="Get actuator value",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device and/or actuator with given ID not found."
                },
                status.HTTP_504_GATEWAY_TIMEOUT: {
                    "model": schemas.Detail,
                    "description": "The value could not be read within the set timeout."
                }
            })
async def get_actuator_value(device_id: int = Path(..., description="The ID of the device."),
                             actuator_id: int = Path(..., description="The ID of the actuator.")):
    """
    Get the value for the specified actuator of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return await asyncio.wait_for(device.actuators[actuator_id].get_value(), timeout=get_timeout)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail=f"The value could not be read within the timeout of {get_timeout} s.")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")


@router.put("/{actuator_id}/value", response_model=Union[str, float], summary="Set actuator value",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device and/or actuator with given ID not found."
                },
                status.HTTP_504_GATEWAY_TIMEOUT: {
                    "model": schemas.Detail,
                    "description": "The value could not be set within the set timeout."
                },
                status.HTTP_406_NOT_ACCEPTABLE: {
                    "model": schemas.Detail,
                    "description": "The value to set was not within the set limits."
                },
                status.HTTP_423_LOCKED: {
                    "model": schemas.Detail,
                    "description": "The device is busy."
                }
            })
async def set_actuator_value(value: Union[int, float] = Query(..., description="The value to set the actuator to."),
                             device_id: int = Path(..., description="The ID of the device."),
                             actuator_id: int = Path(..., description="The ID of the actuator.")):
    """
    Set the value for the specified actuator of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        await asyncio.wait_for(device.actuators[actuator_id].set_value(value), timeout=set_timeout)
        try:
            return await asyncio.wait_for(device.actuators[actuator_id].get_value(), timeout=get_timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                                detail=f"The set could not be read within the timeout of {get_timeout} s.")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")
    except FastMDAisBusy:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="The device is busy.")
    except FastMDAatHardSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the hard limits of the setting " +
                                   f"{device.actuators[actuator_id].get_hard_limits()}")
    except FastMDAatSoftSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the soft limits of the setting " +
                                   f"{device.actuators[actuator_id].get_soft_limits()}")
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail=f"The value of {value} could not be set within the timeout of {set_timeout} s.")


@router.get("/{actuator_id}/settings",
            response_model=List[Union[schemas.DiscreteSettingInfo, schemas.ContinuousSettingInfo]],
            summary="Get all actuator settings",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device and/or actuator with given ID not found."
                }
            })
async def get_all_actuator_settings(device_id: int = Path(..., description="The ID of the device."),
                                    actuator_id: int = Path(..., description="The ID of the actuator.")):
    """
    Get a list of information on all the settings for the specified detector of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return [setting.info for _, setting in device.actuators[actuator_id].settings.items()]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")


@router.get("/{actuator_id}/setting/{setting_id}",
            response_model=Union[schemas.DiscreteSettingInfo, schemas.ContinuousSettingInfo],
            summary="Get actuator setting information",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device, actuator and/or setting with given ID not found."
                }
            })
async def get_actuator_setting(device_id: int = Path(..., description="The ID of the device."),
                               actuator_id: int = Path(..., description="The ID of the actuator."),
                               setting_id: int = Path(..., description="The ID of the setting.")):
    """
    Get the setting information for the specified setting for the specified actuator of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        actuator = device.actuators[actuator_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")
    try:
        return actuator.settings[setting_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator setting with ID {setting_id}.")


@router.get("/{actuator_id}/setting/{setting_id}/value", response_model=Union[str, float],
            summary="Get actuator setting value",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device, actuator and/or setting with given ID not found."
                },
                status.HTTP_504_GATEWAY_TIMEOUT: {
                    "model": schemas.Detail,
                    "description": "The value could not be read within the set timeout."
                }
            })
async def get_actuator_setting_value(device_id: int = Path(..., description="The ID of the device."),
                                     actuator_id: int = Path(..., description="The ID of the actuator."),
                                     setting_id: int = Path(..., description="The ID of the setting.")):
    """
    Get the setting value for the specified setting for the specified actuator of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        actuator = device.actuators[actuator_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")
    try:
        return await asyncio.wait_for(actuator.settings[setting_id].get_value(), timeout=set_timeout)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail=f"The value could not be read within the timeout of {get_timeout} s.")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator setting with ID {setting_id}.")


@router.put("/{actuator_id}/setting/{setting_id}/value", response_model=Union[str, float],
            summary="Set actuator setting value",
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "model": schemas.Detail,
                    "description": "Device, actuator and/or setting with given ID not found."
                },
                status.HTTP_504_GATEWAY_TIMEOUT: {
                    "model": schemas.Detail,
                    "description": "The value could not be set within the set timeout."
                },
                status.HTTP_406_NOT_ACCEPTABLE: {
                    "model": schemas.Detail,
                    "description": "The value to set was not within the set limits."
                },
                status.HTTP_423_LOCKED: {
                    "model": schemas.Detail,
                    "description": "The device is busy."
                }
            })
async def set_actuator_setting_value(
        value: Union[int, float] = Query(..., description="The value to set the setting to."),
        device_id: int = Path(..., description="The ID of the device."),
        actuator_id: int = Path(..., description="The ID of the actuator."),
        setting_id: int = Path(..., description="The ID of the setting.")
):
    """
    Set the setting value for the specified setting for the specified actuator of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        actuator = device.actuators[actuator_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")
    try:
        await asyncio.wait_for(actuator.settings[setting_id].set_value(value), timeout=set_timeout)
        try:
            return await asyncio.wait_for(actuator.settings[setting_id].get_value(), timeout=set_timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                                detail=f"The set could not be read within the timeout of {get_timeout} s.")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator setting with ID {setting_id}.")
    except FastMDAisBusy:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="The device is busy.")
    except FastMDAatHardSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the hard limits of the setting " +
                                   f"{actuator.settings[setting_id].get_hard_limits()}")
    except FastMDAatSoftSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the soft limits of the setting " +
                                   f"{actuator.settings[setting_id].get_soft_limits()}")
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail=f"The value of {value} could not be set within the timeout of {set_timeout} s.")
