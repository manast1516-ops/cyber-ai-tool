from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class ToolResult(BaseModel):
    tool_name: str
    status: str
    data: Dict[str, Any]
    error: Optional[str] = None

class BaseSecurityTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        pass
