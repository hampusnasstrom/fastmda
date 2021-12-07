from typing import List, Union

from fastapi import APIRouter, Path, HTTPException, status, Query

from fastmda import schemas
from fastmda.exceptions import *
from fastmda.globals import device_dict

router = APIRouter(
    prefix="/devices/{device_id}/detectors",
    tags=["detectors"]
)


@router.get("/", response_model=List[schemas.DetectorInfo], summary="Get all added detector instances")
async def get_all_detectors(device_id: int = Path(..., description="The ID of the device.")):
    """
    Get a list of information for all the added detector instances for the specified device.
    """
    try:
        return [det.info for _, det in device_dict[device_id].detectors.items()]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")


@router.get("/{detector_id}", response_model=schemas.DetectorInfo, summary="Get detector information")
async def get_detector(device_id: int = Path(..., description="The ID of the device."),
                       detector_id: int = Path(..., description="The ID of the detector.")):
    """
    Get the information for the specified detector of the the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return device.detectors[detector_id].info
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector with ID {detector_id}.")


@router.get("/{detector_id}/settings",
            response_model=List[Union[schemas.DiscreteSettingInfo, schemas.ContinuousSettingInfo]],
            summary="Get all detector settings")
async def get_all_detector_settings(device_id: int = Path(..., description="The ID of the device."),
                                    detector_id: int = Path(..., description="The ID of the detector.")):
    """
    Get a list of information on all the settings for the specified detector of the the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return [setting.info for _, setting in device.detectors[detector_id].settings]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector with ID {detector_id}.")


@router.get("/{detector_id}/setting/{setting_id}",
            response_model=Union[schemas.DiscreteSettingInfo, schemas.ContinuousSettingInfo],
            summary="Get detector setting information")
async def get_detector_setting(device_id: int = Path(..., description="The ID of the device."),
                               detector_id: int = Path(..., description="The ID of the detector."),
                               setting_id: int = Path(..., description="The ID of the setting.")):
    """
    Get the setting information for the specified setting for the specified detector of the the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        detector = device.detectors[detector_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector with ID {detector_id}.")
    try:
        return detector.settings[setting_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector setting with ID {setting_id}.")


@router.get("/{detector_id}/setting/{setting_id}/value", response_model=Union[str, float],
            summary="Get detector setting value")
async def get_detector_setting_value(device_id: int = Path(..., description="The ID of the device."),
                                     detector_id: int = Path(..., description="The ID of the detector."),
                                     setting_id: int = Path(..., description="The ID of the setting.")):
    """
    Get the setting value for the specified setting for the specified detector of the the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        detector = device.detectors[detector_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector with ID {detector_id}.")
    try:
        return detector.settings[setting_id].get_value()
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector setting with ID {setting_id}.")


@router.put("/{detector_id}/setting/{setting_id}/value", response_model=Union[str, float],
            summary="Set detector setting value")
async def set_detector_setting_value(
        value: Union[int, float] = Query(..., description="The value to set the setting to."),
        device_id: int = Path(..., description="The ID of the device."),
        detector_id: int = Path(..., description="The ID of the detector."),
        setting_id: int = Path(..., description="The ID of the setting.")
):
    """
    Set the setting value for the specified setting for the specified detector of the the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        detector = device.detectors[detector_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector with ID {detector_id}.")
    try:
        detector.settings[setting_id].set_value(value)
        return detector.settings[setting_id].get_value()
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No detector setting with ID {setting_id}.")
    except FastMDAisBusy:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail=f"The device is busy.")
    except FastMDAatHardSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the hard limits of the setting " +
                                   f"{detector.settings[setting_id].get_hard_limits()}")
    except FastMDAatSoftSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the soft limits of the setting " +
                                   f"{detector.settings[setting_id].get_soft_limits()}")
