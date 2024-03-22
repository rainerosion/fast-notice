import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, ResponseValidationError
from pydantic_core import ValidationError
from starlette.responses import JSONResponse

from app.api.main import router
from app.core.exceptions import BusinessException, UnauthorizedException, ForbiddenException
from app.core.resp import Result

app = FastAPI(
    debug=True,
)


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


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exception):
    """
    deal with validation exception
    :param request:
    :param exception:
    :return:
    """
    validation_info = [{'field': error['loc'][0], 'message': error['msg']} for error in exception.errors()]
    error = Result.error(code=422, msg="Validation Error.", data=validation_info)
    return JSONResponse(
        content=error.dict(),
        status_code=422
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


@app.exception_handler(Exception)
async def other_exception_handler(request, exception):
    """
    deal with other exception
    :param request:
    :param exception:
    :return:
    """
    error = Result.error(code=500, msg="Internal Server Error")
    return JSONResponse(
        content=error.dict(),
        status_code=500
    )


app.include_router(router)
# app.include_router(item.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
