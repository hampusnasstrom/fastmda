from typing import Dict, Optional, Any

from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    name: str
    device_type: str = Field(...,
                             description="The type of device, corresponds to the python script where the Device " +
                                         "class is defined without the .py extension")
    args: Dict[str, Any]
    is_connected: Optional[bool] = False
