from fastapi import FastAPI

from fastmda.devices import example_device
from fastmda.schemas import DeviceInfo

description = """
This is the OpenAPI interface for the fastMDA multi dimensional acquisition server

"""

tags_metadata = [
    {
        "name": "devices",
        "description": "Operations with devices",
    },
    {
        "name": "users",
        "description": "Manage users."
    },
]

app = FastAPI(
    title="fastMDA",
    description=description,
    version="0.0.1",
    contact={
        "name": "Hampus Näsström",
        "email": "hampus.nasstrom@gmail.com",
    },
    openapi_tags=tags_metadata
)

device_info = {
    1: DeviceInfo(
        name="Some device",
        args={
            "com_port": "COM1"
        }
    )
}
device_dict = {}

from fastmda.routers import devices
app.include_router(devices.router)


@app.on_event("startup")
async def build_device_dict():
    for device_id in device_info:
        device_dict[device_id] = example_device.Device(**device_info[device_id].args)


@app.on_event("shutdown")
async def disconnect_devices():
    for device_id in device_dict:
        if device_info[device_id].is_connected:
            device_dict[device_id].disconnect()
