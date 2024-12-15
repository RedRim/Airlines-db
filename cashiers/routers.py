from fastapi import APIRouter, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates

from admin.schemas import SaleTicketAddSchema
from admin import queires as Q
from admin.responses_data import HTMLField, SaleTicketFields
from auth.token import get_user_id
from admin.query_config import CashierColumnsConfig

from tickets.query_config import IndexTicketsConfig
from .queries import CashiersQueries

from datetime import datetime


router = APIRouter()

@router.get('/sale_ticket/{id}', response_class=HTMLResponse)
def add_sale_ticket_form(request: Request,
                    id: int,
                    cashier_id: int = Depends(get_user_id),):
    fields = SaleTicketFields(
        ticket = HTMLField(
            label = 'ID билета',
            field_name = 'ticket',
            field_id = 'ticket',
            type = 'text',
            value=id,
        ),
        client = HTMLField(
            label = 'ID клиента',
            field_name = 'client',
            field_id = 'client',
            type = 'text',
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'билета',
        'route': 'cashiers',
        'cashier_id': cashier_id,
        }
    
    

    return templates.TemplateResponse("cashiers/sale_ticket.html", response_dict)

@router.post('/sale_ticket/{cashier_id}', response_class=HTMLResponse)
def add_sale_ticket(request: Request,
          data: Annotated[SaleTicketAddSchema, Form()],
          cashier_id: int):
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    Connect.execute(Q.SaleTicketQueries.add_sale_ticket(
        data.ticket, cashier_id, data.client, today_date,
    ))

    redirect_response = RedirectResponse(url='/', status_code=303)

    return redirect_response

@router.get("/cashier_profile/{cashier_id}", response_class=HTMLResponse)
def client_profile(request: Request,
                   cashier_id: int):

    client = Connect.fetchone(Q.CashiersQueries.get_cashier(cashier_id))
    tickets_rows = Connect.fetchall(CashiersQueries.get_cashier_tickets(cashier_id))

    tickets = {}
    cols = IndexTicketsConfig
    for ticket in tickets_rows:
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

    return templates.TemplateResponse("cashiers/profile.html", {
        "request": request,
        'passport_number': client[CashierColumnsConfig.passport_number.value],
        'passport_series': client[CashierColumnsConfig.passport_series.value],
        'first_name': client[CashierColumnsConfig.first_name.value],
        'last_name': client[CashierColumnsConfig.last_name.value],
        'middle_name': client[CashierColumnsConfig.middle_name.value],
        'email': client[CashierColumnsConfig.email.value],
        'tickets': tickets.values(),
    })