from pydantic import BaseModel
from fastapi import Form

class Base(BaseModel):
    ...

class ClientAddSchema(Base):
    email: str = Form(None)
    passport_number: int = Form(None)
    passport_series: int = Form(None)
    first_name: str = Form(None)
    last_name: str = Form(None)
    middle_name: str = Form(None)
    password: str = Form(None)


class ClientEditSchema(ClientAddSchema):
    id: int = Form(None)
    role: int = Form(None)


class AirlineAddSchema(Base):
    name: str = Form(None)
    city: str = Form(None)
    street: str = Form(None)
    house: str = Form(None)

class AirlineEditSchema(AirlineAddSchema):
    ...
    