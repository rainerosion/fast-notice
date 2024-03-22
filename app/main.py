import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic_core import ValidationError
from starlette.responses import JSONResponse

from app.api.main import router
from app.core.config import settings
from app.core.exceptions import BusinessException, UnauthorizedException, ForbiddenException
from app.core.resp import Result

app = FastAPI(
    debug=False,
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)


@app.exception_handler(Exception)
async def exception_handler(request, exception):
    """
    deal with various exceptions
    :param request:
    :param exception:
    :return:
    """
    if isinstance(exception, BusinessException):
        status_code = 405
    elif isinstance(exception, UnauthorizedException):
        status_code = 401
    elif isinstance(exception, ForbiddenException):
        status_code = 403
    elif isinstance(exception, RequestValidationError) or isinstance(exception, ValidationError):
        status_code = 422
    elif isinstance(exception, HTTPException):
        status_code = exception.status_code
    else:
        status_code = 500

    if hasattr(exception, 'error_code') and hasattr(exception, 'message'):
        error = Result.error(code=exception.error_code, msg=exception.message)
    elif hasattr(exception, 'detail'):
        error = Result.error(code=status_code, msg=exception.detail)
    else:
        error = Result.error(code=500, msg="Internal Server Error")

    return JSONResponse(content=error.dict(), status_code=status_code)


app.include_router(router)
# app.include_router(item.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
