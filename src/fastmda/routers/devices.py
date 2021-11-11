from typing import Dict

from fastapi import APIRouter, Path, HTTPException, status, Depends
from sqlalchemy.orm import Session

from fastmda import crud
from fastmda.database import SessionLocal
from fastmda.exceptions import FastMDAConnectFailed, FastMDAImplementationError
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
