from fastapi import APIRouter, Form, HTTPException, Response, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt
from jose.exceptions import JWTError

from .schemas import ClientRegisterSchema, ClientLoginSchema
from .queries import Auth, AllEmailsQueries
from .tocken import get_current_user_data, create_token, role_required

from settings import security, config, templates
from database.connection import Connect

router = APIRouter()

@router.get('/register', response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post('/register', response_class=HTMLResponse)
def process_registration(request: Request,
                        email: str = Form(None),
                        passport_num: int = Form(None),
                        passport_series: int = Form(None),
                        first_name: str = Form(None),
                        last_name: str = Form(None),
                        middle_name: str = Form(None),
                        password: str = Form(None)):
    existing_emails = Connect.fetchall(AllEmailsQueries.get_all(email))
    if existing_emails:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": "Email уже используется.",
        })

    user = Connect.fetchone(
        Auth.register_client(
            passport_num,
            passport_series,
            first_name,
            last_name,
            middle_name,
            password,
            email,
        )
    )
    token = create_token(email=email, user_id=user[0], role=user[1])

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
          email: str = Form(None),
          password: str = Form(None),):
    result = Connect.fetchone(Auth.login(email))
    if not result:
        raise HTTPException(status_code=401, detail="Неверный email")
    q_email, q_password, q_role, q_id = result[0].strip(), result[1].strip(), result[2], result[3]
    if password != q_password:
        raise HTTPException(status_code=401, detail="Неверный пароль")

    token = create_token(email=q_email, user_id=q_id, role=q_role)
    print(token)

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
    # Используем RedirectResponse без явного указания метода
    return RedirectResponse(url='/login', status_code=302)