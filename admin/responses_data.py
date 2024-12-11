from dataclasses import dataclass

@dataclass
class HTMLField:
    label: str
    field_name: str
    field_id: str
    value: str
    type: str

@dataclass
class ClientFields:
    id: HTMLField
    passport_number: HTMLField
    passport_series: HTMLField
    first_name: HTMLField
    last_name: HTMLField
    middle_name: HTMLField
    role: HTMLField
    email: HTMLField

@dataclass
class AdminFields:
    id: HTMLField
    username: HTMLField
    role: HTMLField
    email: HTMLField

@dataclass
class AirlinesFields:
    id: HTMLField
    name: HTMLField
    city: HTMLField
    street: HTMLField
    house: HTMLField

@dataclass
class CashiersFields:
    id: HTMLField
    ticket_office: HTMLField
    first_name: HTMLField
    last_name: HTMLField
    middle_name: HTMLField
    password: HTMLField
    role: HTMLField
    email: HTMLField

@dataclass
class CouponesFields:
    id: HTMLField
    departure: HTMLField
    destination: HTMLField
    fare: HTMLField
    ticket: HTMLField
    num: HTMLField
    flight_time: HTMLField

@dataclass
class SaleTicketFields:
    id: HTMLField
    ticket: HTMLField
    cashier: HTMLField
    client: HTMLField
    sale_date: HTMLField

@dataclass
class TicketOfficesFields:
    id: HTMLField
    city: HTMLField
    street: HTMLField
    house: HTMLField

@dataclass
class TicketsFields:
    id: HTMLField
    type: HTMLField
    airline: HTMLField