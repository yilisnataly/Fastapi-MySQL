from typing import Optional
from pydantic import BaseModel #pydantic permite añadir tipos de datos y Base Model para modelar los datos


class Student(BaseModel):
    id: Optional[int]
    name: str
    email: str
    phone: str
    address: str
