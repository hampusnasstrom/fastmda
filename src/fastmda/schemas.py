from typing import Dict, Optional, Any

from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    name: str
    script: str = Field(..., description="The name of the python script where the Device class is defined")
    args: Dict[str, Any]
    is_connected: Optional[bool] = False
