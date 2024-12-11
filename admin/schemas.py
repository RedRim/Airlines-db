from pydantic import BaseModel
from fastapi import Form

class Base(BaseModel):
    ...

class ClientEditSchema(Base):
    id: int = Form(None)
    email: str = Form(None)
    passport_number: int = Form(None)
    passport_series: int = Form(None)
    first_name: str = Form(None)
    last_name: str = Form(None)
    middle_name: str = Form(None)
    role: int = Form(None)