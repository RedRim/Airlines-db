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
import airlines.database.crud as Q 

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
@app.post("/", response_class=HTMLResponse)
async def index(request: Request, airline_id: int = Form(None)):
    airline = None
    if airline_id is not None:
        airline = get_airline_by_id(airline_id)
        print(airline)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "airline_id": airline_id,
        "airline": airline[0],
    })


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)