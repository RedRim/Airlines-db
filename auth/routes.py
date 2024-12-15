from fastapi import APIRouter, Form, HTTPException, Response, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from .schemas import ClientRegisterSchema, ClientLoginSchema
from .queries import Auth, AllEmailsQueries
from .token import get_current_user_data, create_token

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

    redirect_response = RedirectResponse(url='/home', status_code=303)

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

    redirect_response = RedirectResponse(url='/home', status_code=303)

    redirect_response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite='lax',
        secure=False
    )

    return redirect_response

@router.get('/home', response_class=HTMLResponse)
def home(request: Request, data: dict = Depends(get_current_user_data)):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "email": data['email'],
        'id': data['id'],
    })


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(config.JWT_HEADER_NAME)
    return RedirectResponse(url='/login', status_code=302)