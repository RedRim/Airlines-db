from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from .clients import router as clients_router
from .airlines import router as airlines_router
from settings import templates

router = APIRouter()

router.include_router(clients_router, prefix='/clients')
router.include_router(airlines_router, prefix='/airlines')

@router.get('/', response_class=HTMLResponse)
def tables(request: Request):
    routes = {
        'clients': 'Пользователи',
        'cashiers': 'Кассиры',
        'admins': 'Администраторы',
        'airlines': 'Авиакомпании',
        'tickets': 'Билеты',
        'coupones': 'Купоны',
        'ticket_offices': 'Кассы',
        'sales_ticket': 'Продажи билетов',
    }

    return templates.TemplateResponse('admin/tables.html', {'request': request, 'routes': routes})
