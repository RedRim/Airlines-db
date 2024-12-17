from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import pandas as pd
import io

from pydantic import BaseModel 
from typing import Annotated

from .queires import TaskQueries
from database.connection import Connect
from settings import templates
from auth.token import role_required

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def all_tasks(request: Request, user = Depends(role_required([0])),):
        return templates.TemplateResponse("admin/task/tasks.html", {
        "request": request,
    })

class MonthAirline(BaseModel):
    month: int = Form(None)
    airline: str = Form(None)

@router.get("/month", response_class=HTMLResponse)
def month_tickets(request: Request, user = Depends(role_required([0])),):
        return templates.TemplateResponse("admin/task/month_tickets.html", {
        "request": request,
    })

@router.post("/download/month")
async def download_data(request: Request, data: Annotated[MonthAirline, Form()]):
    rows = Connect.fetchall(TaskQueries.month_tickets(month=data.month, airline_name=data.airline))
    df = pd.DataFrame.from_records(rows)
    df.columns = ["ИД билета", "Номер месяца"]
    
    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name='Билеты')
    output.seek(0)
    
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=tickets.xlsx"})



@router.get("/sales_volume", response_class=HTMLResponse)
def sales_volume(request: Request, user = Depends(role_required([0])),):
        return templates.TemplateResponse("admin/task/sales_volumes.html", {
        "request": request,
    })


@router.post("/download/sales_volume")
async def sales_volume_data(request: Request):
    rows = Connect.fetchall(TaskQueries.sales_volume())
    df = pd.DataFrame.from_records(rows)
    df.columns = ["Сумма тарифа", "Авиакомпания"]
    
    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name='Объем продаж')
    output.seek(0)
    
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=sales_volume.xlsx"})



class ClientsOnDate(BaseModel):
    date: str = Form(None)
    airline: str = Form(None)

@router.get("/clients", response_class=HTMLResponse)
def clients_on_date(request: Request, user = Depends(role_required([0])),):
        return templates.TemplateResponse("admin/task/clients_on_date.html", {
        "request": request,
    })

@router.post("/download/clients_on_date")
async def download_clients_on_date(request: Request, data: Annotated[ClientsOnDate, Form()]):
    rows = Connect.fetchall(TaskQueries.clients_on_date(date=data.date, airline=data.airline))
    df = pd.DataFrame.from_records(rows)
    df.columns = ["Имя", "Дата"]
    
    output = io.BytesIO()
    df.to_excel(output, index=False, sheet_name='Клиенты')
    output.seek(0)
    
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=clients_on_date.xlsx"})
