from fastapi import HTTPException, Response, Depends, Request
from jose import jwt
from jose.exceptions import JWTError

from settings import security, config

def get_current_user_data(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('id')
        email = payload.get('sub')
        role = payload.get('role')
        return {'email': email, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    
def create_token(email: str, user_id: int, role: int):
    """Создание токена(при авторизации)"""
    payload = {
        'id': user_id,
        'role': role,
    }

    token = security.create_access_token(uid=email, data=payload)

    return token

def get_user_role(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        return -1  # токен отсутствует
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
        role = payload.get('role')
        return role
    except JWTError:
        return -1  # токен недействителен

def get_user_id(request: Request):
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    if not token:
        return -1  # токен отсутствует
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
        id = payload.get('id')
        return id
    except JWTError:
        return -1  


def role_required(allowed_roles: list[int]):
    """
    Проверяет, что роль пользователя входит в список разрешенных ролей.
    """
    def dependency(user_data: dict = Depends(get_current_user_data)):
        if user_data['role'] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user_data
    return dependency

def get_token_data(token: str):
    payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
    return payload