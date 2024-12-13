from dataclasses import dataclass

@dataclass
class HTMLField:
    label: str
    field_name: str
    field_id: str
    type: str
    value: str = ''

@dataclass
class ClientFields:
    passport_number: HTMLField
    passport_series: HTMLField
    first_name: HTMLField
    last_name: HTMLField
    middle_name: HTMLField
    role: HTMLField
    email: HTMLField
    password: HTMLField

@dataclass
class AdminFields:
    username: HTMLField
    role: HTMLField
    email: HTMLField

@dataclass
class AirlinesFields:
    name: HTMLField
    city: HTMLField
    street: HTMLField
    house: HTMLField

@dataclass
class CashiersFields:
    ticket_office: HTMLField
    first_name: HTMLField
    last_name: HTMLField
    middle_name: HTMLField
    password: HTMLField
    role: HTMLField
    email: HTMLField

@dataclass
class CouponesFields:
    departure: HTMLField
    destination: HTMLField
    fare: HTMLField
    ticket: HTMLField
    num: HTMLField
    flight_time: HTMLField

@dataclass
class SaleTicketFields:
    ticket: HTMLField
    cashier: HTMLField
    client: HTMLField
    sale_date: HTMLField

@dataclass
class TicketOfficesFields:
    city: HTMLField
    street: HTMLField
    house: HTMLField

@dataclass
class TicketFields:
    type: HTMLField
    airline: HTMLField