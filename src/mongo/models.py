from pydantic import BaseModel
from typing import Any, Optional, List


class Counter(BaseModel):
    id: Optional[Any]
    phrase: str
    region_id: int


class Result(BaseModel):
    counter_id: str
    count: int
    top_ads: str
    timestamp: int
