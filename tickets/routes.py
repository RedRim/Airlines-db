from fastapi import APIRouter, Form, Request, Depends
from fastapi import Form, Request
from fastapi.responses import HTMLResponse

from database.connection import Connect
from .queries import TicketsQueries
from database.query_config import IndexTicketsConfig
from auth.token import get_user_role

from settings import templates


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index_get(request: Request):
    return templates.TemplateResponse("tickets.html", {
        "request": request,
        'tickets': None,
    })

@router.post("/", response_class=HTMLResponse)
def index_post(request: Request,
                role: int = Depends(get_user_role),
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

    rows = Connect.fetchall(TicketsQueries.get_all(departure_date_from=departure_date_from, 
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

    redirect_routes = {
        0: '/admin',
        1: '/cashiers/sale_ticket',
        2: '/clients/tickets_offices',
        -1: '/login',
    }



    return templates.TemplateResponse("tickets.html", {
        "request": request,
        'tickets': tickets.values(),
        'departure_date_from': departure_date_from,
        'departure_date_to': departure_date_to,
        'departure': departure,
        'destination': destination,
        'redirect_route': redirect_routes[role],
    })