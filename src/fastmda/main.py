import importlib
import os

from fastapi import FastAPI

from fastmda.exceptions import FastMDAImplementationError, FastMDAModuleError
from fastmda.globals import *

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
        module_name = f"fastmda.devices.{device_info[device_id].device_type}"
        try:
            device_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise FastMDAModuleError(module_name)
        try:
            device_dict[device_id] = device_module.Device(**device_info[device_id].args)
        except AttributeError:
            raise FastMDAImplementationError(device_module, "No Device class implementation.")


@app.on_event("shutdown")
async def disconnect_devices():
    for device_id in device_dict:
        if device_info[device_id].is_connected:
            device_dict[device_id].disconnect()
