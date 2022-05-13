import json
from typing import List

from sqlalchemy.orm import Session

from fastmda import models, schemas


def get_device_infos(db: Session, skip: int = 0, limit: int = 100) -> List[models.DeviceInfo]:
    return db.query(models.DeviceInfo).offset(skip).limit(limit).all()


def get_device_info(db: Session, device_id: int) -> models.DeviceInfo:
    return db.query(models.DeviceInfo).filter(models.DeviceInfo.id == device_id).first()


def create_device_info(db: Session, device_info: schemas.DeviceInfoCreate) -> models.DeviceInfo:
    db_device_info = models.DeviceInfo(**device_info.dict(), is_connected=False)
    db.add(db_device_info)
    db.commit()
    db.refresh(db_device_info)
    return db_device_info


def update_device_connection_status(db: Session, device_id: int, connection_status: bool):
    device_info = get_device_info(db, device_id)
    if device_info is not None:
        device_info.is_connected = connection_status
        db.commit()
        return device_info
    else:
        return None
