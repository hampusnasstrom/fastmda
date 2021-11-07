from fastapi import APIRouter, Path, HTTPException, status

from fastmda.exceptions import FastMDAConnectFailed
from fastmda.main import device_info, device_dict
from fastmda.schemas import DeviceInfo

router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)


@router.get("/{device_id}", response_model=DeviceInfo)
async def get_devices(device_id: int = Path(..., description="The id of the device")):
    if device_id not in device_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    return device_info[device_id]


@router.put("/{device_id}/connect")
async def connect_device(device_id: int = Path(..., description="The id of the device")):
    if device_id not in device_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    try:
        device_info[device_id].is_connected = device_dict[device_id].connect()
    except NotImplementedError:
        return {"error": "Device class has not implemented connect method"}
    except FastMDAConnectFailed as e:
        return {"error": e}
    return {"connection_status": device_info[device_id].is_connected}


@router.put("/{device_id}/disconnect")
async def disconnect_device(device_id: int = Path(..., description="The id of the device")):
    if device_id not in device_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    try:
        device_info[device_id].is_connected = not device_dict[device_id].disconnect()
    except NotImplementedError:
        return {"error": "Device class has not implemented disconnect method"}
    return {"connection_status": device_info[device_id].is_connected}
