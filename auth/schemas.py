from pydantic import BaseModel
from fastapi import Form

class Base(BaseModel):
    ...

class ClientRegisterSchema(Base):
    email: str = Form(None)
    passport_num: int = Form(None)
    passport_series: int = Form(None)
    first_name: str = Form(None)
    last_name: str = Form(None)
    middle_name: str = Form(None)
    password: str = Form(None)

class ClientLoginSchema(Base):
    email: str = Form(None)
    password: str = Form(None)
    