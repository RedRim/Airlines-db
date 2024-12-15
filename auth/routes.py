from fastapi import APIRouter, Form, HTTPException, Response, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .schemas import ClientRegisterSchema, ClientLoginSchema
from .queries import Auth, AllEmailsQueries
from .token import get_current_user_data, create_token, get_user_id, get_user_role
import admin.queires as Q
import admin.query_config as QC
from tickets.queries import TicketsQueries
from tickets.query_config import IndexTicketsConfig

from settings import security, config, templates
from database.connection import Connect

from typing import Annotated

router = APIRouter()

@router.get('/register', response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post('/register', response_class=HTMLResponse)
def register(request: Request,
                        data: Annotated[ClientRegisterSchema, Form()]):
    existing_emails = Connect.fetchall(AllEmailsQueries.get_all(data.email))
    if existing_emails:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "Email уже используется.",
        })

    user = Connect.fetchone(
        Auth.register_client(
            data.passport_num,
            data.passport_series,
            data.first_name,
            data.last_name,
            data.middle_name,
            data.password,
            data.email,
        )
    )
    token = create_token(email=data.email, user_id=user[0], role=user[1])

    redirect_response = RedirectResponse(url='/profile', status_code=303)

    redirect_response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite='lax',
        secure=False
    )

    return redirect_response


@router.get('/login', response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post('/login', response_class=HTMLResponse)
def login(request: Request,
          data: Annotated[ClientLoginSchema, Form()],):
    result = Connect.fetchone(Auth.login(data.email))
    if not result:
        raise HTTPException(status_code=401, detail="Неверный email")
    q_email, q_password, q_role, q_id = result[0].strip(), result[1].strip(), result[2], result[3]
    if data.password != q_password:
        raise HTTPException(status_code=401, detail="Неверный пароль")

    token = create_token(email=q_email, user_id=q_id, role=q_role)

    redirect_response = RedirectResponse(url='/profile', status_code=303)

    redirect_response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite='lax',
        secure=False
    )

    return redirect_response


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(config.JWT_HEADER_NAME)
    return RedirectResponse(url='/login', status_code=302)

@router.get("/profile", response_class=HTMLResponse,)
def client_profile(request: Request,
                   user_id: int = Depends(get_user_id),
                   user_role: int = Depends(get_user_role)):
    if user_role == 2:
        client = Connect.fetchone(Q.ClientsQueries.get_client(user_id))
        columns_response = [
            client[QC.ClientColumnsConfig.passport_number.value],
            client[QC.ClientColumnsConfig.passport_series.value],
            client[QC.ClientColumnsConfig.first_name.value],
            client[QC.ClientColumnsConfig.last_name.value],
            client[QC.ClientColumnsConfig.middle_name.value],
            client[QC.ClientColumnsConfig.email.value],
        ]
        fields = ['Номер паспорта', "Серия паспорта", "Имя", "Фамилия", "Отчество", "Почта"]
        zero_tickets_text = 'У вас нет купленных билетов'
        user_name = client[QC.ClientColumnsConfig.first_name.value]
    elif user_role == 1:
        cashier = Connect.fetchone(Q.CashiersQueries.get_cashier(user_id))
        columns_response = [
            cashier[QC.CashierColumnsConfig.ticket_office.value],
            cashier[QC.CashierColumnsConfig.first_name.value],
            cashier[QC.CashierColumnsConfig.last_name.value],
            cashier[QC.CashierColumnsConfig.middle_name.value],
            cashier[QC.CashierColumnsConfig.email.value],
        ]
        fields = ['Касса', "Имя", "Фамилия", "Отчество", "Почта"]
        zero_tickets_text = 'У вас нет проданных билетов'
        user_name = cashier[QC.CashierColumnsConfig.first_name.value]
    else:
        return templates.TemplateResponse("auth/login.html", {"request": request})
    tickets_rows = Connect.fetchall(TicketsQueries.get_user_tickets(user_id, user_role))

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

    return templates.TemplateResponse("auth/profile.html", {
        "request": request,
        'columns_response': columns_response,
        'fields': enumerate(fields),
        'tickets': tickets.values(),
        'zero_tickets_text': zero_tickets_text,
        'user_name': user_name,
    })