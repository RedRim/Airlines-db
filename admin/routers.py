from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from .tables.clients import router as clients_router
from .tables.airlines import router as airlines_router
from .tables.tickets import router as tickets_router
from .tables.coupones import router as coupones_router
from settings import templates

router = APIRouter()

router.include_router(clients_router, prefix='/clients')
router.include_router(airlines_router, prefix='/airlines')
router.include_router(tickets_router, prefix='/tickets')
router.include_router(coupones_router, prefix='/coupones')


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
