import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.api.main import router
from app.core.exceptions import BusinessException, UnauthorizedException, ForbiddenException
from app.core.resp import Result

app = FastAPI()


@app.exception_handler(BusinessException)
async def business_exception_handler(request, exception):
    """
    deal with business exception
    :param request:
    :param exception:
    :return:
    """
    error = Result.error(code=exception.error_code, msg=exception.message)
    return JSONResponse(
        content=error.dict(),
        status_code=405
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request, exception):
    """
    deal with unauthorized exception
    :param request:
    :param exception:
    :return:
    """
    error = Result.error(code=exception.error_code, msg=exception.message)
    return JSONResponse(
        content=error.dict(),
        status_code=401
    )


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request, exception):
    """
    deal with unauthorized exception
    :param request:
    :param exception:
    :return:
    """
    error = Result.error(code=exception.error_code, msg=exception.message)
    return JSONResponse(
        content=error.dict(),
        status_code=403
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exception):
    """
    deal with other http exception
    :param request:
    :param exception:
    :return:
    """
    error = Result.error(code=exception.status_code, msg=exception.detail)
    return JSONResponse(
        content=error.dict(),
        status_code=exception.status_code
    )


app.include_router(router)
# app.include_router(item.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
