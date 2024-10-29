from fastapi import FastAPI

from api.users.handlers import router as user_router


def init_app() -> FastAPI:
    app = FastAPI(
        title='TestCase',
        docs_url='/api/docs',
        debug=True,
    )

    app.include_router(user_router, prefix='/api')
    return app