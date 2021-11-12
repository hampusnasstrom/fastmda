from typing import Dict, List, Union

from fastapi import APIRouter, Path, HTTPException, status, Depends
from sqlalchemy.orm import Session

from fastmda import crud, schemas
from fastmda.database import SessionLocal
from fastmda.exceptions import FastMDAConnectFailed, FastMDAImplementationError
from fastmda.globals import device_dict, device_types_info, device_types_modules
from fastmda.objects import DiscreteActuator, ContinuousActuator

router = APIRouter(
    prefix="/devices/{device_id}/actuators",
    tags=["actuators"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/discrete", response_model=List[schemas.DiscreteActuatorInfo])
async def get_discrete_actuators(device_id: int = Path(..., description="The ID of the device.")):
    try:
        return [act.info for _, act in device_dict[device_id].actuators.items() if isinstance(act, DiscreteActuator)]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")


@router.get("/continuous", response_model=List[schemas.ContinuousActuatorInfo])
async def get_continuous_actuators(device_id: int = Path(..., description="The ID of the device.")):
    try:
        return [act.info for _, act in device_dict[device_id].actuators.items() if isinstance(act, ContinuousActuator)]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")


@router.get("/{actuator_id}", response_model=Union[schemas.DiscreteActuatorInfo, schemas.ContinuousActuatorInfo])
async def get_actuator(device_id: int = Path(..., description="The ID of the device."),
                       actuator_id: int = Path(..., description="The ID of the actuator.")):
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return device.actuators[actuator_id].info
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")


@router.get("/{actuator_id}/value", response_model=Union[str, float])
async def get_actuator_value(device_id: int = Path(..., description="The ID of the device."),
                             actuator_id: int = Path(..., description="The ID of the actuator.")):
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return device.actuators[actuator_id].get_value()
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")


@router.put("/{actuator_id}/value", response_model=Union[str, float])
async def set_actuator_value(value: Union[int, float],
                             device_id: int = Path(..., description="The ID of the device."),
                             actuator_id: int = Path(..., description="The ID of the actuator.")):
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        device.actuators[actuator_id].set_value(value)
        return device.actuators[actuator_id].get_value()
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No actuator with ID {actuator_id}.")
