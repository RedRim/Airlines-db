from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from settings import Settings, security, config, templates

from tickets.routes import router as tickets_router
from admin.routers import router as admin_router
from auth.routes import router as auth_router
from clients.routers import router as clients_router
from cashiers.routers import router as cashier_router


app = FastAPI(title=Settings.app_name, debug=Settings.debug)

# app.mount(Settings.static_url, StaticFiles(directory=Settings.static_dir), name='static')

app.include_router(tickets_router, prefix='', tags=['Tickets'])
app.include_router(admin_router, prefix='/admin', tags=['Admin'])
app.include_router(auth_router, prefix='', tags=['Auth'])
app.include_router(clients_router, prefix='/clients', tags=['Clients'])
app.include_router(cashier_router, prefix='/cashiers', tags=['Cashiers'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)