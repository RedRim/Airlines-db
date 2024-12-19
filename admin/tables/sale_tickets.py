from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request


from database.connection import Connect
from settings import templates
from auth.token import role_required

from admin import queires as Q


router = APIRouter()


@router.get('/', response_class=HTMLResponse)
def ticket_offices(request: Request, user = Depends(role_required([0])),):
    columns = [
        'ID',
        'Билет',
        'Кассир',
        'Клиент',
        "Дата продажи",
    ]

    ticket_offices = Connect.fetchall(Q.SaleTicketQueries.get_all())

    return templates.TemplateResponse('admin/records.html',
                                      {'request': request,
                                       'columns': columns,
                                       'len_cols': len(columns),
                                       'records': ticket_offices,
                                       'edit_route': 'sale_tickets',
                                       'case_name': 'Продажами билетов'})