from fastapi import APIRouter, Form, HTTPException, Response, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt
from jose.exceptions import JWTError

from .schemas import ClientRegisterSchema, ClientLoginSchema
from settings import security, config, templates
from .queries import Auth, AllEmailsQueries

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

    Connect.execute(
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
    token = security.create_access_token(uid=email)

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
          response: Response,
          email: str = Form(None),
          password: str = Form(None),):
    result = Connect.fetchone(Auth.login_client(email))
    if not result:
        raise HTTPException(status_code=401, detail="Неверный email")
    q_email, q_password = result[0].strip(), result[1].strip()
    if password != q_password:
        raise HTTPException(status_code=401, detail="Неверный пароль")

    token = security.create_access_token(uid=q_email)

    redirect_response = RedirectResponse(url='/home', status_code=303)

    redirect_response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite='lax',
        secure=False
    )

    return redirect_response


def get_current_user(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
        email = payload.get("sub")
        print(payload)
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token 1")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token 2")

@router.get('/home', response_class=HTMLResponse)
def home(request: Request, email: str = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {
        "request": request,
        "email": email,
    })


@router.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "Доступ разрешен."}