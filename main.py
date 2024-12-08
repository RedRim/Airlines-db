from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
import uvicorn

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from settings import DATABASE_CONFIG
from database.connection import Connect
import database.crud as Q
from database.pages import IndexTicketsQueries 
from database.query_config import IndexTicketsConfig

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class AirlineParams(BaseModel):
    name: str
    city: str
    street: str
    house: str

@app.get("/airlines", response_model=List[dict])
def get_airlines():
    res = Connect.execute(Q.AirlinesQueries.get_all())
    return res

@app.post("/airlines/")
def add_airline(airline: AirlineParams):
    res = Connect.execute(Q.AirlinesQueries.add_airline(
        airline.name,
        airline.city,
        airline.street,
        airline.house,
    ))

    return res

@app.put("/airlines/{id}")
def update_airline(airline: AirlineParams):
    res = Connect.execute(Q.AirlinesQueries.update_airline(
        airline.name,
        airline.city,
        airline.street,
        airline.house,
    ))
    return res

@app.delete("/airlines/{id}")
def delete_airline(id: int):
    res = Connect.execute(Q.AirlinesQueries.delete_airline(id))
    return res

def get_airline_by_id(airline_id):
    airline = Connect.execute(f"SELECT * FROM airlines WHERE id = {airline_id}")
    return airline



@app.get("/", response_class=HTMLResponse)
def index_get(request: Request):
    return templates.TemplateResponse("tickets.html", {
        "request": request,
        'tickets': None,
    })

@app.post("/", response_class=HTMLResponse)
def index_post(request: Request,
                departure_date_from: str = Form(None),
                departure_date_to: str = Form(None),
                departure: str = Form(None),
                destination: str = Form(None)):
    
    tickets = {}
    cols = IndexTicketsConfig

    if not (departure_date_from and departure_date_to and departure and destination):
        return templates.TemplateResponse("tickets.html", {
            "request": request,
            'tickets': None,
            'error_message': 'Пожалуйста, заполните все поля.',
            'departure_date_from': departure_date_from,
            'departure_date_to': departure_date_to,
            'departure': departure,
            'destination': destination
        })

    rows = Connect.execute(IndexTicketsQueries.get_all(departure_date_from=departure_date_from, 
                                                       departure_date_to=departure_date_to,
                                                       departure=departure,
                                                       destination=destination))
    
    for ticket in rows:
        ticket_id = ticket[cols.TICKET_ID.value]
        if ticket_id not in tickets:
            tickets[ticket_id] = {}
            tickets[ticket_id]['id'] = ticket[cols.TICKET_ID.value]
            tickets[ticket_id]['route'] = f'{ticket[cols.DEPARTURE.value]} - {ticket[cols.DESTINATION.value]}'
            tickets[ticket_id]['fare'] = float(ticket[cols.TOTAL_FARE.value])
            tickets[ticket_id]['type'] = 'Эконом' if ticket[cols.TICKET_TYPE.value] == 1 else 'Бизнес'
            tickets[ticket_id]['airline'] = ticket[cols.AIRLINE_NAME.value]
            tickets[ticket_id]['flight_time'] = ticket[cols.FLIGHT_TIME.value].strftime('%Y-%m-%d %H:%M')
        else:
            tickets[ticket_id]['route'] += f' - {ticket[cols.DESTINATION.value]}'

    print(tickets)

    return templates.TemplateResponse("tickets.html", {
        "request": request,
        'tickets': tickets.values(),
        'departure_date_from': departure_date_from,
        'departure_date_to': departure_date_to,
        'departure': departure,
        'destination': destination
    })
    



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)