from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from loggers.logger_req import logger
from routers.routes import router

app = FastAPI()

@app.middleware("http")
async def logging_middleware(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code} {response.headers}")
    return response

@app.exception_handler(RequestValidationError)
def request_validation_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors(), "body": exc.body},
    )


app.include_router(router)