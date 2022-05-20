from sqlalchemy import Boolean, Column, Integer, String, PickleType

from .database import Base


class DeviceInfo(Base):
    __tablename__ = "device_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    device_type = Column(String, index=True)
    args = Column(PickleType, index=True)
    is_connected = Column(Boolean, index=True)
