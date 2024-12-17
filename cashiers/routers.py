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
from auth.token import get_user_id, role_required
from admin.query_config import CashierColumnsConfig

from tickets.query_config import IndexTicketsConfig
from .queries import CashiersQueries

from datetime import datetime


router = APIRouter()

@router.get('/sale_ticket/{id}', response_class=HTMLResponse)
def add_sale_ticket_form(
                    request: Request,
                    id: int,
                    user = Depends(role_required([1])),
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
          cashier_id: int, user = Depends(role_required([1])),):
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    Connect.execute(Q.SaleTicketQueries.add_sale_ticket(
        data.ticket, cashier_id, data.client, today_date,
    ))

    redirect_response = RedirectResponse(url='/', status_code=303)

    return redirect_response
