import importlib
import os
from pkgutil import iter_modules

from fastapi import FastAPI, Depends

from fastmda.exceptions import FastMDAImplementationError, FastMDAModuleError
from fastmda.globals import *
from fastmda import models, device_types, crud
from fastmda.database import engine, SessionLocal
from fastmda.schemas import DeviceInfo
from fastmda.routers import devices

from sqlalchemy.orm import Session

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

models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def build_device_dict():
    for device_module_info in iter_modules(device_types.__path__):
        module_name = f"fastmda.device_types.{device_module_info.name}"
        try:
            device_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise FastMDAModuleError(module_name)
        try:
            device_type = device_module.Device.device_type
        except AttributeError:
            raise FastMDAImplementationError(device_module, "Does not subclass AbstractDevice.")
        device_types_info[device_module_info.name] = device_type
        device_types_modules[device_module_info.name] = device_module
    with SessionLocal() as db:
        device_infos = crud.get_device_infos(db, limit=999)
        for device_info_orm in device_infos:
            device_info = DeviceInfo.from_orm(device_info_orm)
            device_module = device_types_modules[device_info.device_type]
            try:
                device_dict[device_info.id] = device_module.Device(**device_info.args)
                device_info_orm.is_connected = device_dict[device_info.id].is_connected()
                db.commit()
            except AttributeError:
                raise FastMDAImplementationError(device_module, "No Device class implementation.")


@app.on_event("shutdown")
async def disconnect_devices():
    print("Got here")
    # Disconnect all devices
    with SessionLocal() as db:
        for device_id in device_dict:
            device_dict[device_id].disconnect()
            crud.update_device_connection_status(db, device_id, False)
        # db.query(models.DeviceInfo).update({"is_connected": False})
