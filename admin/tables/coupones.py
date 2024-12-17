from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates
from auth.token import role_required

from admin.schemas import CouponeAddSchema, CouponeEditSchema
from admin import queires as Q
from admin.responses_data import HTMLField, CouponesFields
from admin.query_config import CouponesColumnsConfig


router = APIRouter()

@router.get('/add', response_class=HTMLResponse)
def add_coupone_form(request: Request, user = Depends(role_required([0])),):
    fields = CouponesFields(
        departure = HTMLField(
            label='Место отправления',
            field_name='departure',
            field_id='departure',
            type='text'
        ),
        destination = HTMLField(
            label='Место прибытия',
            field_name='destination',
            field_id='destination',
            type='text'
        ),
        fare = HTMLField(
            label='Цена',
            field_name='fare',
            field_id='fare',
            type='text'
        ),
        ticket = HTMLField(
            label='ID билета',
            field_name='ticket',
            field_id='ticket',
            type='text'
        ),
        num = HTMLField(
            label='Номер пересадки',
            field_name='num',
            field_id='num',
            type='text'
        ),
        flight_time = HTMLField(
            label='Дата и время вылета',
            field_name='flight_time',
            field_id='flight_time',
            type='datetime-local'
        ),
        duration = HTMLField(
            label='Продолжительность(мин)',
            field_name='duration',
            field_id='duration',
            type='text',
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Купона',
        'route': 'coupones',
        }
    
    

    return templates.TemplateResponse("admin/add_record.html", response_dict)

@router.post('/add', response_class=HTMLResponse)
def add_coupone(request: Request,
          data: Annotated[CouponeAddSchema, Form()], user = Depends(role_required([0])),):
    Connect.execute(Q.CouponesQueries.add_coupone(
        data.departure, data.destination, data.fare, data.ticket, data.num, data.flight_time, data.duration
    ))

    redirect_response = RedirectResponse(url='/admin/coupones', status_code=303)

    return redirect_response

@router.get('/', response_class=HTMLResponse)
def coupones(request: Request, user = Depends(role_required([0])),):
    columns = [
        'ID',
        'Место отправления',
        'Место прибытия',
        'Цена',
        'Билет',
        'Номер пересадки',
        'Дата и время вылета',
        'Продолжительность',
    ]

    coupones = Connect.fetchall(Q.CouponesQueries.get_all())

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': columns,
                                       'len_cols': len(columns),
                                       'records': coupones,
                                       'edit_route': 'coupones',
                                       'case_name': 'Купонами'})


@router.get('/{id}', response_class=HTMLResponse)
def update_coupone_form(id:int, request: Request, user = Depends(role_required([0])),):
    coupone = Connect.fetchone(Q.CouponesQueries.get_coupone(id=id))

    fields = CouponesFields(
        departure = HTMLField(
            label='Место отправления',
            field_name='departure',
            field_id='departure',
            type='text',
            value=coupone[CouponesColumnsConfig.departure.value],
        ),
        destination = HTMLField(
            label='Место прибытия',
            field_name='destination',
            field_id='destination',
            type='text',
            value=coupone[CouponesColumnsConfig.destination.value],
        ),
        fare = HTMLField(
            label='Цена',
            field_name='fare',
            field_id='fare',
            type='text',
            value=coupone[CouponesColumnsConfig.fare.value],
        ),
        ticket = HTMLField(
            label='ID билета',
            field_name='ticket',
            field_id='ticket',
            type='text',
            value=coupone[CouponesColumnsConfig.ticket.value],
        ),
        num = HTMLField(
            label='Номер пересадки',
            field_name='num',
            field_id='num',
            type='text',
            value=coupone[CouponesColumnsConfig.num.value],
        ),
        flight_time = HTMLField(
            label='Дата и время вылета',
            field_name='flight_time',
            field_id='flight_time',
            type='text',
            value=coupone[CouponesColumnsConfig.flight_time.value],
        ),
        duration = HTMLField(
            label='Продолжительность(мин)',
            field_name='duration',
            field_id='duration',
            type='text',
            value=coupone[CouponesColumnsConfig.duration.value],
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Купона',
        'route': 'coupones',
        'id': id,
        } 

    return templates.TemplateResponse("admin/edit_record.html", response_dict)


@router.post('/{id}', response_class=HTMLResponse)
def update_coupone(id: int, request: Request,
          data: Annotated[CouponeEditSchema, Form()], user = Depends(role_required([0])),):
    Connect.execute(Q.CouponesQueries.update_coupone(
        id, data.departure, data.destination, data.fare, data.ticket, data.num, data.flight_time, data.duration
    ))

    redirect_response = RedirectResponse(url='/admin/coupones', status_code=303)

    return redirect_response


@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_coupone(id: int, request: Request, user = Depends(role_required([0])),):
    Connect.execute(Q.CouponesQueries.delete_coupone(id))
    return RedirectResponse(url='/admin/coupones', status_code=303)

