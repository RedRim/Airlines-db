from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates

from admin.schemas import TicketOfficeEditSchema, TicketOfficeAddSchema
from admin import queires as Q
from admin.responses_data import HTMLField, TicketOfficesFields
from admin.query_config import TicketOfficeColumnsConfig


router = APIRouter()

@router.get('/add', response_class=HTMLResponse)
def add__form(request: Request):
    fields = TicketOfficesFields(
        city = HTMLField(
            label='Город',
            field_name='city',
            field_id='city',
            type='text'
        ),
        street = HTMLField(
            label='Улица',
            field_name='street',
            field_id='streeet',
            type='text'
        ),
        house = HTMLField(
            label='Здание',
            field_name='house',
            field_id='house',
            type='text'
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Кассы',
        'route': 'ticket_offices',
        }
    
    

    return templates.TemplateResponse("admin/add_record.html", response_dict)

@router.post('/add', response_class=HTMLResponse)
def add_ticket_offices(request: Request,
          data: Annotated[TicketOfficeAddSchema, Form()]):
    Connect.execute(Q.TicketOfficesQueries.add_ticket_office(
        data.city, data.street, data.house,
    ))

    redirect_response = RedirectResponse(url='/admin/ticket_offices', status_code=303)

    return redirect_response

@router.get('/', response_class=HTMLResponse)
def ticket_offices(request: Request):
    columns = [
        'ID',
        'Город',
        'Улица',
        'Здание',
    ]

    ticket_offices = Connect.fetchall(Q.TicketOfficesQueries.get_all())

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': columns,
                                       'len_cols': len(columns),
                                       'records': ticket_offices,
                                       'edit_route': 'ticket_offices',
                                       'case_name': 'Кассами'})


@router.get('/{id}', response_class=HTMLResponse)
def ticket_offices_form(id:int, request: Request):
    ticket_offices = Connect.fetchone(Q.TicketOfficesQueries.get_ticket_office(id=id))

    fields = TicketOfficesFields(
        city = HTMLField(
            label='Город',
            field_name='city',
            field_id='city',
            value=ticket_offices[TicketOfficeColumnsConfig.city.value],
            type='text'
        ),
        street = HTMLField(
            label='Улица',
            field_name='street',
            field_id='street',
            value=ticket_offices[TicketOfficeColumnsConfig.street.value],
            type='text'
        ),
        house = HTMLField(
            label='Здание',
            field_name='house',
            field_id='house',
            value=ticket_offices[TicketOfficeColumnsConfig.house.value],
            type='text'
        ),
        
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Кассы',
        'route': 'ticket_offices',
        'id': id,
        } 

    return templates.TemplateResponse("admin/edit_record.html", response_dict)


@router.post('/{id}', response_class=HTMLResponse)
def update_ticket_office(id: int, request: Request,
          data: Annotated[TicketOfficeEditSchema, Form()]):
    Connect.execute(Q.TicketOfficesQueries.update_ticket_office(
        id, data.city, data.street, data.house
    ))

    redirect_response = RedirectResponse(url='/admin/ticket_offices', status_code=303)

    return redirect_response


@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_ticket_office(id: int, request: Request):
    Connect.execute(Q.TicketOfficesQueries.delete_ticket_office(id))
    return RedirectResponse(url='/admin/ticket_offices', status_code=303)

