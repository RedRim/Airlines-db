from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates

from admin.schemas import AirlineEditSchema, AirlineAddSchema
from admin import queires as Q
from admin.responses_data import HTMLField, AirlinesFields
from admin.query_config import AirlineColumnsConfig


router = APIRouter()

@router.get('/add', response_class=HTMLResponse)
def add_client_form(request: Request):
    fields = AirlinesFields(
        name = HTMLField(
            label='Название',
            field_name='name',
            field_id='name',
            type='text'
        ),
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
        'case_name': 'Авиакомпании',
        'route': 'airlines',
        }
    
    

    return templates.TemplateResponse("admin/add_record.html", response_dict)

@router.post('/add', response_class=HTMLResponse)
def add_client(request: Request,
          data: Annotated[AirlineAddSchema, Form()]):
    Connect.execute(Q.AirlinesQueries.add_airline(
        data.name, data.city, data.street, data.house,
    ))

    redirect_response = RedirectResponse(url='/admin/airlines', status_code=303)

    return redirect_response

@router.get('/', response_class=HTMLResponse)
def airlines(request: Request):
    columns = [
        'ID',
        'Название',
        'Город',
        'Улица',
        'Здание',
    ]

    airlines = Connect.fetchall(Q.AirlinesQueries.get_all())

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': columns,
                                       'len_cols': len(columns),
                                       'records': airlines,
                                       'edit_route': 'airlines',
                                       'case_name': 'Авиакомпаниями'})


@router.get('/{id}', response_class=HTMLResponse)
def airline_form(id:int, request: Request):
    airline = Connect.fetchone(Q.AirlinesQueries.get_airline(id=id))

    fields = AirlinesFields(
        name = HTMLField(
            label='Название',
            field_name='name',
            field_id='name',
            value=airline[AirlineColumnsConfig.name.value],
            type='text'
        ),
        city = HTMLField(
            label='Город',
            field_name='city',
            field_id='city',
            value=airline[AirlineColumnsConfig.city.value],
            type='text'
        ),
        street = HTMLField(
            label='Улица',
            field_name='street',
            field_id='street',
            value=airline[AirlineColumnsConfig.street.value],
            type='text'
        ),
        house = HTMLField(
            label='Здание',
            field_name='house',
            field_id='house',
            value=airline[AirlineColumnsConfig.house.value],
            type='text'
        ),
        
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Авиакомпании',
        'route': 'airlines',
        'id': id,
        } 

    return templates.TemplateResponse("admin/edit_record.html", response_dict)


@router.post('/{id}', response_class=HTMLResponse)
def update_airline(id: int, request: Request,
          data: Annotated[AirlineEditSchema, Form()]):
    Connect.execute(Q.AirlinesQueries.update_airline(
        id, data.name, data.city, data.street, data.house
    ))

    redirect_response = RedirectResponse(url='/admin/airlines', status_code=303)

    return redirect_response


@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_airline(id: int, request: Request):
    Connect.execute(Q.AirlinesQueries.delete_airline(id))
    return RedirectResponse(url='/admin/airlines', status_code=303)

