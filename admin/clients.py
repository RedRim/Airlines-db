from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates

from .schemas import ClientEditSchema
from . import queires as Q
from .responses_data import HTMLField, ClientFields
from .query_config import ClientColumnsConfig


router = APIRouter()

@router.get('/', response_class=HTMLResponse)
def clients(request: Request):
    columns = [
        'ID',
        'Номер паспорта',
        'Серия паспорта',
        'Имя',
        'Фамилия',
        'Отчество',
        'Права',
        'Почта',
    ]

    clients = Connect.fetchall(Q.ClientsQueries.get_all())
    for idx, client in enumerate(clients):
        print(idx, client)

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': enumerate(columns),
                                       'len_cols': len(columns),
                                       'clients': clients,
                                       'edit_route': 'clients'})


@router.get('/{id}', response_class=HTMLResponse)
def client_form(id:int, request: Request):
    user = Connect.fetchone(Q.ClientsQueries.get_client(id=id))

    fields = ClientFields(
        id = HTMLField(
            label='ID',
            field_name='id',
            field_id='id',
            value=user[ClientColumnsConfig.id.value],
            type='text'
        ),
        passport_number = HTMLField(
            label = 'Номер паспорта',
            field_name = 'passport_number',
            field_id = 'passport_number',
            value = user[ClientColumnsConfig.passport_number.value],
            type = 'text',
        ),
        passport_series = HTMLField(
            label = 'Серия паспорта',
            field_name = 'passport_series',
            field_id = 'passport_series',
            value = user[ClientColumnsConfig.passport_series.value],
            type = 'text',
        ),
        first_name = HTMLField(
            label = 'Имя',
            field_name = 'first_name',
            field_id = 'first_name',
            value = user[ClientColumnsConfig.first_name.value],
            type = 'text',
        ),
        last_name = HTMLField(
            label = 'Фамилия',
            field_name = 'last_name',
            field_id = 'last_name',
            value = user[ClientColumnsConfig.last_name.value],
            type = 'text',
        ),
        middle_name = HTMLField(
            label = 'Отчество',
            field_name = 'middle_name',
            field_id = 'middle_name',
            value = user[ClientColumnsConfig.middle_name.value],
            type = 'text',
        ),
        role = HTMLField(
            label = 'Роль',
            field_name = 'role',
            field_id = 'role',
            value = user[ClientColumnsConfig.role.value],
            type = 'text',
        ),
        email = HTMLField(
            label = 'Email',
            field_name = 'email',
            field_id = 'email',
            value = user[ClientColumnsConfig.email.value],
            type = 'text',
        )
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Пользователя',
        'route': 'clients',
        'id': id,
        }
    
    

    return templates.TemplateResponse("admin/edit_record.html", response_dict)


@router.post('/{id}', response_class=HTMLResponse)
def update_client(id: int, request: Request,
          data: Annotated[ClientEditSchema, Form()]):
    data.email = data.email.strip()
    client_id =  Connect.fetchone(Q.ClientsQueries.update_client(
        data.id, data.email.strip(), data.passport_number, data.passport_series, data.first_name, data.last_name, 
        data.middle_name, data.role
    ))

    redirect_response = RedirectResponse(url='/home', status_code=303)

    return redirect_response


@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_client(id: int, request: Request):
    client = Connect.fetchone(Q.ClientsQueries.get_client(id=id))
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    
    Connect.execute(Q.ClientsQueries.delete_client(id))
    return RedirectResponse(url='/home', status_code=303)

