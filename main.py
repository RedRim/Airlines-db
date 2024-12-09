from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from settings import Settings

from tickets.routes import router as tickets_router
from admin.routers import router as admin_router


app = FastAPI(title=Settings.app_name, debug=Settings.debug)

app.mount(Settings.static_url, StaticFiles(directory=Settings.static_dir), name='static')

app.include_router(tickets_router, prefix='', tags=['Tickets'])
app.include_router(admin_router, prefix='/admin', tags=['Admin'])

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)