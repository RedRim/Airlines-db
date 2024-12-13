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