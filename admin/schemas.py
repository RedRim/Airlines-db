from datetime import datetime
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

class CashierAddSchema(Base):
    ticket_office: int = Form(None)
    first_name: str = Form(None)
    last_name: str = Form(None)
    middle_name: str = Form(None)
    password: str = Form(None)
    email: str = Form(None)
    role: int = Form(None)


class CashierEditSchema(CashierAddSchema):
    ...

class AirlineAddSchema(Base):
    name: str = Form(None)
    city: str = Form(None)
    street: str = Form(None)
    house: str = Form(None)

class AirlineEditSchema(AirlineAddSchema):
    ...
    
class TicketAddSchema(Base):
    type: int = Form(None)
    airline: int = Form(None)

class TicketEditSchema(TicketAddSchema):
    ...

class CouponeAddSchema(Base):
    departure: str = Form(None)
    destination: str = Form(None)
    fare: float = Form(None)
    ticket: int = Form(None)
    num: int = Form(None)
    flight_time: str = Form(None)
    duration: int = Form(None)


class CouponeEditSchema(CouponeAddSchema):
    ...

class TicketOfficeAddSchema(Base):
    city: str = Form(None)
    street: str = Form(None)
    house: str = Form(None)

class TicketOfficeEditSchema(TicketOfficeAddSchema):
    ...

class SaleTicketAddSchema(Base):
    client: int = Form(None)
    ticket: int = Form(None)