import importlib
import os

from fastapi import FastAPI

from globals import *

from fastmda.routers import devices

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

app.include_router(devices.router)


@app.on_event("startup")
async def build_device_dict():
    for device_id in device_info:
        module_file = device_info[device_id].script
        spec = importlib.util.spec_from_file_location(
            module_file[:-3],
            os.path.join("devices", module_file)
        )
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            device_dict[device_id] = module.Device(**device_info[device_id].args)
        except Exception as e:
            print(e)


@app.on_event("shutdown")
async def disconnect_devices():
    for device_id in device_dict:
        if device_info[device_id].is_connected:
            device_dict[device_id].disconnect()
