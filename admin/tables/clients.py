from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates
from auth.token import role_required

from admin.schemas import ClientEditSchema, ClientAddSchema
from admin import queires as Q
from admin.responses_data import HTMLField, ClientFields
from admin.query_config import ClientColumnsConfig


router = APIRouter()

@router.get('/add', response_class=HTMLResponse)
def add_client_form(request: Request, user = Depends(role_required([0])),):
    fields = ClientFields(
        passport_number = HTMLField(
            label = 'Номер паспорта',
            field_name = 'passport_number',
            field_id = 'passport_number',
            type = 'text',
        ),
        passport_series = HTMLField(
            label = 'Серия паспорта',
            field_name = 'passport_series',
            field_id = 'passport_series',
            type = 'text',
        ),
        first_name = HTMLField(
            label = 'Имя',
            field_name = 'first_name',
            field_id = 'first_name',
            type = 'text',
        ),
        last_name = HTMLField(
            label = 'Фамилия',
            field_name = 'last_name',
            field_id = 'last_name',
            type = 'text',
        ),
        middle_name = HTMLField(
            label = 'Отчество',
            field_name = 'middle_name',
            field_id = 'middle_name',
            type = 'text',
        ),
        role = HTMLField(
            label = 'Роль',
            field_name = 'role',
            field_id = 'role',
            type = 'text',
            value = 2,
        ),
        email = HTMLField(
            label = 'Email',
            field_name = 'email',
            field_id = 'email',
            type = 'text',
        ),
        password = HTMLField(
            label = 'Пароль',
            field_name = 'passoword',
            field_id = 'password',
            type = 'password',
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Пользователя',
        'route': 'clients',
        }
    
    

    return templates.TemplateResponse("admin/add_record.html", response_dict)

@router.post('/add', response_class=HTMLResponse)
def add_client(request: Request,
          data: Annotated[ClientAddSchema, Form()], user = Depends(role_required([0])),):
    data.email = data.email.strip()
    Connect.execute(Q.ClientsQueries.add_client(
        data.email, data.password, data.passport_number, data.passport_series, data.first_name, data.last_name, 
        data.middle_name
    ))

    redirect_response = RedirectResponse(url='/admin/clients', status_code=303)

    return redirect_response

@router.get('/', response_class=HTMLResponse)
def clients(request: Request, user = Depends(role_required([0])),):
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

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': columns,
                                       'len_cols': len(columns),
                                       'records': clients,
                                       'edit_route': 'clients',
                                       'case_name': 'Пользователями'})


@router.get('/{id}', response_class=HTMLResponse)
def client_form(id:int, request: Request, user = Depends(role_required([0])),):
    user = Connect.fetchone(Q.ClientsQueries.get_client(id=id))

    fields = ClientFields(
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
          data: Annotated[ClientEditSchema, Form()], user = Depends(role_required([0])),):
    data.email = data.email.strip()
    Connect.execute(Q.ClientsQueries.update_client(
        id, data.email, data.passport_number, data.passport_series, data.first_name, data.last_name, 
        data.middle_name, data.role
    ))

    redirect_response = RedirectResponse(url='/admin/clients', status_code=303)

    return redirect_response




@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_client(id: int, request: Request, user = Depends(role_required([0])),):
    Connect.execute(Q.ClientsQueries.delete_client(id))
    return RedirectResponse(url='/admin/clients', status_code=303)
