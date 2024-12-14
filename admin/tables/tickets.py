from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates

from admin.schemas import TicketAddSchema, TicketEditSchema
from admin import queires as Q
from admin.responses_data import HTMLField, TicketFields
from admin.query_config import TicketsColumnsConfig


router = APIRouter()

@router.get('/add', response_class=HTMLResponse)
def add_ticket_form(request: Request):
    fields = TicketFields(
        type = HTMLField(
            label='Класс',
            field_name='type',
            field_id='type',
            type='text'
        ),
        airline = HTMLField(
            label='ID Авиакомпании',
            field_name='airline',
            field_id='airline',
            type='text'
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Билета',
        'route': 'tickets',
        }
    
    

    return templates.TemplateResponse("admin/add_record.html", response_dict)

@router.post('/add', response_class=HTMLResponse)
def add_ticket(request: Request,
          data: Annotated[TicketAddSchema, Form()]):
    Connect.execute(Q.TicketsQueries.add_ticket(
        data.type, data.airline,
    ))

    redirect_response = RedirectResponse(url='/admin/tickets', status_code=303)

    return redirect_response

@router.get('/', response_class=HTMLResponse)
def tickets(request: Request):
    columns = [
        'ID',
        'Класс',
        'Авиакомпания',
    ]

    tickets = Connect.fetchall(Q.TicketsQueries.get_all())

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': columns,
                                       'len_cols': len(columns),
                                       'records': tickets,
                                       'edit_route': 'tickets',
                                       'case_name': 'Билетами'})


@router.get('/{id}', response_class=HTMLResponse)
def update_ticket_form(id:int, request: Request):
    ticket = Connect.fetchone(Q.TicketsQueries.get_ticket(id=id))

    fields = TicketFields(
        type = HTMLField(
            label='Класс',
            field_name='type',
            field_id='type',
            type='text',
            value=ticket[TicketsColumnsConfig.type.value],
        ),
        airline = HTMLField(
            label='ID Авиакомпании',
            field_name='airline',
            field_id='airline',
            type='text',
            value=ticket[TicketsColumnsConfig.airline.value],
        ),
        
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Билета',
        'route': 'tickets',
        'id': id,
        } 

    return templates.TemplateResponse("admin/edit_record.html", response_dict)


@router.post('/{id}', response_class=HTMLResponse)
def update_ticket(id: int, request: Request,
          data: Annotated[TicketEditSchema, Form()]):
    Connect.execute(Q.TicketsQueries.update_ticket(
        id, data.type, data.airline
    ))

    redirect_response = RedirectResponse(url='/admin/tickets', status_code=303)

    return redirect_response


@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_ticket(id: int, request: Request):
    Connect.execute(Q.TicketsQueries.delete_ticket(id))
    return RedirectResponse(url='/admin/tickets', status_code=303)

