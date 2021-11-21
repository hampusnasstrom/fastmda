from typing import Dict, List, Union

from fastapi import APIRouter, Path, HTTPException, status, Depends, Query

from fastmda import crud, schemas
from fastmda.exceptions import FastMDAConnectFailed, FastMDAImplementationError
from fastmda.globals import device_dict, device_types_info, device_types_modules
from fastmda.objects import DiscreteActuator, ContinuousActuator

router = APIRouter(
    prefix="/devices/{device_id}/detectors",
    tags=["detectors"]
)


@router.get("/", response_model=List[schemas.DetectorInfo])
async def get_all_detectors(device_id: int = Path(..., description="The ID of the device.")):
    try:
        return [det.info for _, det in device_dict[device_id].detectors.items()]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")


@router.get("/{detector_id}", response_model=schemas.DetectorInfo)
async def get_detector(device_id: int = Path(..., description="The ID of the device."),
                       detector_id: int = Path(..., description="The ID of the detector.")):
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return device.detectors[detector_id].info
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector with ID {detector_id}.")
