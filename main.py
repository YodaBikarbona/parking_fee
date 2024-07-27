import uvicorn

from main.api.app import app
from main.api.base.base import initialize_database

from main.api.user.controller.register_controller import router as register_router
from main.api.user.controller.login_controller import router as login_router
from main.api.ticket.controller.ticket_controller import router as ticket_router

app.include_router(register_router)
app.include_router(login_router)
app.include_router(ticket_router)


if __name__ == "__main__":
    initialize_database()
    uvicorn.run(app=app, port=8000, log_level="info")
