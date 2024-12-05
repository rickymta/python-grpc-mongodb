from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime

@dataclass
class Todo:
    id: Optional[str] = None
    title: str = ""
    message: str = ""
    inner_log: Optional[Dict[str, str]] = None  # Thêm trường inner_log
    created_at: datetime = datetime.utcnow()
