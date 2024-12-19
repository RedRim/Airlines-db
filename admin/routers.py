from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from .tables.clients import router as clients_router
from .tables.airlines import router as airlines_router
from .tables.tickets import router as tickets_router
from .tables.coupones import router as coupones_router
from .tables.ticket_offices import router as ticket_offices_router
from .tables.cashiers import router as cashiers_router
from .tables.sale_tickets import router as sale_tickets_router
from .task_routers import router as task_router
from settings import templates
from auth.token import role_required

router = APIRouter()

router.include_router(clients_router, prefix='/clients')
router.include_router(airlines_router, prefix='/airlines')
router.include_router(tickets_router, prefix='/tickets')
router.include_router(coupones_router, prefix='/coupones')
router.include_router(ticket_offices_router, prefix='/ticket_offices')
router.include_router(cashiers_router, prefix='/cashiers')
router.include_router(sale_tickets_router, prefix='/sales_ticket')
router.include_router(task_router, prefix='/task')


@router.get('/', response_class=HTMLResponse)
def tables(request: Request, user = Depends(role_required([0]))):
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
