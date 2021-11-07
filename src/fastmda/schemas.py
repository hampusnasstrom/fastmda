from typing import Dict, Optional, Any

from pydantic import BaseModel


class DeviceInfo(BaseModel):
    name: str
    args: Dict[str, Any]
    is_connected: Optional[bool] = False
