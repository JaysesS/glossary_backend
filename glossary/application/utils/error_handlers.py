from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from glossary.src.core.exception.base import AuthError, CrudError

def auth_error_handler(app: FastAPI):
    @app.exception_handler(AuthError)
    def exception_handler(request: Request, exc: AuthError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)}
        )

def crud_error_handler(app: FastAPI):
    @app.exception_handler(CrudError)
    def exception_handler(request: Request, exc: CrudError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)}
        )

def unhandled_error_handler(app: FastAPI):
    @app.exception_handler(Exception)
    def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Unhandled error!"}
        )

HANDLERS = [
    auth_error_handler,
    crud_error_handler,
    unhandled_error_handler,
]

def register_error_handlers(app: FastAPI):
    for handler in HANDLERS:
        handler(app)
