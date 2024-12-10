from fastapi import APIRouter

from pydantic import BaseModel
from typing import List

from database.connection import Connect
import database.crud as Q

router = APIRouter()


@router.get("/airlines", response_model=List[dict])
def get_airlines():
    res = Connect.fetchall(Q.AirlinesQueries.get_all())
    return res

class AirlineParams(BaseModel):
    name: str
    city: str
    street: str
    house: str

@router.post("/airlines/")
def add_airline(airline: AirlineParams):
    res = Connect.fetchall(Q.AirlinesQueries.add_airline(
        airline.name,
        airline.city,
        airline.street,
        airline.house,
    ))

    return res

@router.put("/airlines/{id}")
def update_airline(airline: AirlineParams):
    res = Connect.fetchall(Q.AirlinesQueries.update_airline(
        airline.name,
        airline.city,
        airline.street,
        airline.house,
    ))
    return res

@router.delete("/airlines/{id}")
def delete_airline(id: int):
    res = Connect.fetchall(Q.AirlinesQueries.delete_airline(id))
    return res

def get_airline_by_id(airline_id):
    airline = Connect.fetchall(f"SELECT * FROM airlines WHERE id = {airline_id}")
    return airline