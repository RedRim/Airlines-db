from enum import Enum

class ClientColumnsConfig(Enum):
    id = 0
    passport_number = 1
    passport_series = 2
    first_name = 3
    last_name = 4
    middle_name = 5
    role = 6
    email = 7

class AirlineColumnsConfig(Enum):
    id = 0
    name = 1
    city = 2
    street = 3
    house = 4

class TicketsColumnsConfig(Enum):
    id = 0
    type = 1
    airline = 2

class CouponesColumnsConfig(Enum):
    id = 0
    departure = 1
    destination = 2
    fare = 3
    ticket = 4
    num = 5
    flight_time = 6 

class TicketOfficeColumnsConfig(Enum):
    id = 0
    city = 1
    street = 2
    house = 3

