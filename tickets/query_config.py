from enum import Enum

class CouponesConfig(Enum):
    departure = 0
    destination = 1
    fare = 2
    num = 3
    type = 4
    flight_time = 5
    destination_time = 6
    time = 7

class IndexTicketsConfig(Enum):
    TICKET_ID = 0
    NUM = 1
    AIRLINE_NAME = 2
    TICKET_TYPE = 3
    DEPARTURE = 4
    DESTINATION = 5
    FLIGHT_TIME = 6
    TOTAL_FARE = 7
    START_POINT = 8
    END_POINT = 9