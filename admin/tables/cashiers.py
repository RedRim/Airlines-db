from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request

from typing import Annotated
from dataclasses import asdict

from database.connection import Connect
from settings import templates
from auth.token import role_required

from admin.schemas import CashierAddSchema, CashierEditSchema
from admin import queires as Q
from admin.responses_data import HTMLField, CashiersFields
from admin.query_config import CashierColumnsConfig



router = APIRouter()

@router.get('/add', response_class=HTMLResponse)
def add_cashier_form(request: Request, user = Depends(role_required([0])),):
    fields = CashiersFields(
        ticket_office = HTMLField(
            label='Касса',
            field_name='ticket_office',
            field_id = 'ticket_office',
            type = 'text'
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
        password = HTMLField(
            label = 'Пароль',
            field_name = 'passoword',
            field_id = 'password',
            type = 'password',
        ),
        role = HTMLField(
            label = 'Роль',
            field_name = 'role',
            field_id = 'role',
            type = 'text',
            value = 1,
        ),
        email = HTMLField(
            label = 'Email',
            field_name = 'email',
            field_id = 'email',
            type = 'text',
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Кассира',
        'route': 'cashiers',
        }

    return templates.TemplateResponse("admin/add_record.html", response_dict)

@router.post('/add', response_class=HTMLResponse)
def add_cashier(request: Request,
          data: Annotated[CashierAddSchema, Form()], user = Depends(role_required([0])),):
    data.email = data.email.strip()
    Connect.execute(Q.CashiersQueries.add_cashier(
        data.ticket_office, data.first_name, data.last_name, 
        data.middle_name, data.password, data.email, data.role,
    ))

    redirect_response = RedirectResponse(url='/admin/cashiers', status_code=303)

    return redirect_response

@router.get('/', response_class=HTMLResponse)
def cashiers(request: Request, user = Depends(role_required([0])),):
    columns = [
        'ID',
        'Касса',
        'Имя',
        'Фамилия',
        'Отчество',
        'Права',
        'Почта',
    ]

    cashiers = Connect.fetchall(Q.CashiersQueries.get_all())

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': columns,
                                       'len_cols': len(columns),
                                       'records': cashiers,
                                       'edit_route': 'cashiers',
                                       'case_name': 'Кассирами'})


@router.get('/{id}', response_class=HTMLResponse)
def cashier_form(id:int, request: Request):
    cashier = Connect.fetchone(Q.CashiersQueries.get_cashier(id=id), user = Depends(role_required([0])),)

    fields = CashiersFields(
        ticket_office = HTMLField(
            label='Касса',
            field_name='ticket_office',
            field_id = 'ticket_office',
            type = 'text',
            value=cashier[CashierColumnsConfig.ticket_office.value],
        ),
        first_name = HTMLField(
            label = 'Имя',
            field_name = 'first_name',
            field_id = 'first_name',
            type = 'text',
            value=cashier[CashierColumnsConfig.first_name.value],
        ),
        last_name = HTMLField(
            label = 'Фамилия',
            field_name = 'last_name',
            field_id = 'last_name',
            type = 'text',
            value=cashier[CashierColumnsConfig.last_name.value],
        ),
        middle_name = HTMLField(
            label = 'Отчество',
            field_name = 'middle_name',
            field_id = 'middle_name',
            type = 'text',
            value=cashier[CashierColumnsConfig.middle_name.value],
        ),
        role = HTMLField(
            label = 'Роль',
            field_name = 'role',
            field_id = 'role',
            type = 'text',
            value=cashier[CashierColumnsConfig.role.value],
        ),
        email = HTMLField(
            label = 'Email',
            field_name = 'email',
            field_id = 'email',
            type = 'text',
            value=cashier[CashierColumnsConfig.email.value],
        ),
    )

    response_dict = {
        "request": request, 
        'fields': asdict(fields),
        'case_name': 'Кассира',
        'route': 'cashiers',
        'id': id,
        }
    
    

    return templates.TemplateResponse("admin/edit_record.html", response_dict)


@router.post('/{id}', response_class=HTMLResponse)
def update_cashier(id: int, request: Request,
          data: Annotated[CashierEditSchema, Form()], user = Depends(role_required([0])),):
    data.email = data.email.strip()
    Connect.execute(Q.CashiersQueries.update_cashier(
        id, data.ticket_office, data.first_name, data.last_name, 
        data.middle_name, data.email, data.role,
    ))

    redirect_response = RedirectResponse(url='/admin/cashiers', status_code=303)

    return redirect_response




@router.post('/delete/{id}', response_class=HTMLResponse)
def delete_cashier(id: int, request: Request, user = Depends(role_required([0])),):
    Connect.execute(Q.CashiersQueries.delete_cashier(id))
    return RedirectResponse(url='/admin/cashiers', status_code=303)
