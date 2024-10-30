from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.users.handlers import router as user_router
from exeptions.base import ApplicationException


async def application_exception_handler(request: Request, exc: ApplicationException):
    return JSONResponse(
        status_code=exc.error_code,
        content={"message": exc.message}
    )

def init_app() -> FastAPI:
    app = FastAPI(
        title='TestCase',
        docs_url='/api/docs',
        debug=True,
    )

    app.include_router(user_router, prefix='/api')
    app.add_exception_handler(ApplicationException, application_exception_handler)
    return app