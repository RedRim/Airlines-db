from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse

from settings import templates
from admin.queires import TicketOfficesQueries
from admin.query_config import TicketOfficeColumnsConfig
from database.connection import Connect


router = APIRouter()

@router.get("/ticket_offices", response_class=HTMLResponse)
def ticket_offices(request: Request):

    ticket_offices_rows = Connect.fetchall(TicketOfficesQueries.get_all())
    ticket_offices = [
        {'city' :row[TicketOfficeColumnsConfig.city.value],
        'street': row[TicketOfficeColumnsConfig.street.value],
        'house': row[TicketOfficeColumnsConfig.house.value]}
        for row in ticket_offices_rows
    ]

    return templates.TemplateResponse("clients/ticket_offices.html", {
        "request": request,
        'ticket_offices': ticket_offices,
    })
