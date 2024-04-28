from pydantic import BaseModel
from typing import Optional

class Korgi(BaseModel):
    id: Optional[int]
    name: str
    age: int
    description: Optional[str]
    price: float  # Добавление поля цены в модель данных
