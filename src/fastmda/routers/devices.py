from typing import Dict, List, Union

from fastapi import APIRouter, Path, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from fastmda import crud, schemas
from fastmda.database import SessionLocal
from fastmda.exceptions import *
from fastmda.globals import device_dict, device_types_info, device_types_modules
from fastmda.schemas import DeviceInfo, DeviceType, DeviceInfoCreate

router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[DeviceInfo])
async def get_devices(db: Session = Depends(get_db)):
    return crud.get_device_infos(db)


@router.get("/device_types", response_model=Dict[str, DeviceType])
async def get_device_types():
    return device_types_info


@router.get("/{device_id}", response_model=DeviceInfo)
async def get_device(device_id: int = Path(..., description="The id of the device"), db: Session = Depends(get_db)):
    device_info = crud.get_device_info(db, device_id)
    if device_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return device_info


@router.post("/add_device", response_model=DeviceInfo, status_code=status.HTTP_201_CREATED)
async def add_device(device_info: DeviceInfoCreate, db: Session = Depends(get_db)):
    device_info_orm = crud.create_device_info(db, device_info)
    device_info = DeviceInfo.from_orm(device_info_orm)
    device_module = device_types_modules[device_info.device_type]
    try:
        device_dict[device_info.id] = device_module.Device(device_info.id, **device_info.args)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                            detail=f'{device_module.__name__} has not implemented a Device class.')
    except TypeError as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                            detail=f'{device_module.__name__} has not implemented Device class according to spec. {e}')
    return device_info


@router.put("/{device_id}/connect", response_model=DeviceInfo)
async def connect_device(device_id: int = Path(..., description="The id of the device"), db: Session = Depends(get_db)):
    device_info = crud.get_device_info(db, device_id)
    if device_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    try:
        if device_dict[device_id].connect():
            return crud.update_device_connection_status(db, device_id, device_dict[device_id].is_connected())
    except NotImplementedError:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                            detail="Device class has not implemented connect method")
    except FastMDAConnectFailed as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e)
    return device_info


@router.put("/{device_id}/disconnect", response_model=DeviceInfo)
async def disconnect_device(device_id: int = Path(..., description="The id of the device"),
                            db: Session = Depends(get_db)):
    device_info = crud.get_device_info(db, device_id)
    if device_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    try:
        if device_dict[device_id].disconnect():
            device_info = crud.update_device_connection_status(db, device_id, device_dict[device_id].is_connected())
    except NotImplementedError:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                            detail="Device class has not implemented disconnect method")
    except FastMDAConnectFailed as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e)
    return device_info


@router.get("/{device_id}/settings",
            response_model=List[Union[schemas.DiscreteSettingInfo, schemas.ContinuousSettingInfo]],
            summary="Get all device settings")
async def get_all_device_settings(device_id: int = Path(..., description="The ID of the device.")):
    """
    Get a list of information on all the settings for the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    return [setting.info for _, setting in device.settings]


@router.get("/{device_id}/setting/{setting_id}",
            response_model=Union[schemas.DiscreteSettingInfo, schemas.ContinuousSettingInfo],
            summary="Get device setting information")
async def get_device_setting(device_id: int = Path(..., description="The ID of the device."),
                             setting_id: int = Path(..., description="The ID of the setting.")):
    """
    Get the setting information for the specified setting of the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return device.settings[setting_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device setting with ID {setting_id}.")


@router.get("/{device_id}/setting/{setting_id}/value", response_model=Union[str, float],
            summary="Get device setting value")
async def get_device_setting_value(device_id: int = Path(..., description="The ID of the device."),
                                   setting_id: int = Path(..., description="The ID of the setting.")):
    """
    Get the setting value for the specified setting of the the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        return device.settings[setting_id].get_value()
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device setting with ID {setting_id}.")


@router.put("/{device_id}/setting/{setting_id}/value", response_model=Union[str, float],
            summary="Set device setting value")
async def set_device_setting_value(
        value: Union[int, float] = Query(..., description="The value to set the setting to."),
        device_id: int = Path(..., description="The ID of the device."),
        setting_id: int = Path(..., description="The ID of the setting.")
):
    """
    Set the setting value for the specified setting of the the specified device.
    """
    try:
        device = device_dict[device_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with ID {device_id}.")
    try:
        device.settings[setting_id].set_value(value)
        return device.settings[setting_id].get_value()
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device setting with ID {setting_id}.")
    except FastMDAisBusy:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail=f"The device is busy.")
    except FastMDAatHardSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the hard limits of the setting " +
                                   f"{device.settings[setting_id].get_hard_limits()}")
    except FastMDAatSoftSettingLimit:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The value of {value} is outside the soft limits of the setting " +
                                   f"{device.settings[setting_id].get_soft_limits()}")
