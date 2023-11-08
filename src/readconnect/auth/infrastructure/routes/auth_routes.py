from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from readconnect.shared.domain.dtos.error_response_dto import ErrorResponse
from readconnect.shared.domain.exceptions.exceptions import (
    NotFoundError,
    InvalidsCredentialsError,
)
from ...application.login_user.login_user_use_case import LoginUserUseCase
from ...application.signup_user.signup_user_use_case import SignupUserUseCase
from ...domain.dtos.login_request_dto import LoginRequestDTO
from ...domain.dtos.login_response_dto import LoginResponseDTO
from ...domain.dtos.signup_request_dto import SignupRequestDTO

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    path="/login",
    responses={
        200: {"model": LoginResponseDTO},
        502: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def login(
    body: LoginRequestDTO,
    login_use_case: Annotated[LoginUserUseCase, Depends(LoginUserUseCase)],
):
    try:
        response = await login_use_case.execute(body)
        return response
    except ValidationError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
    except InvalidsCredentialsError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.details}"
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
    except NotFoundError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.details}"
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
    except Exception as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )


@auth_router.post(
    path="/signup",
    responses={
        200: {"model": SignupRequestDTO},
        502: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def signup(
    body: SignupRequestDTO,
    signup_use_case: Annotated[SignupUserUseCase, Depends(SignupUserUseCase)],
):
    try:
        response = await signup_use_case.execute(body)
        return response

    except ValidationError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
    except InvalidsCredentialsError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.details}"
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )

    except NotFoundError as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.details}"
        return JSONResponse(
            status_code=e.status_code,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
    except Exception as e:
        details = f"Ocurrió un problema al realizar su petición. Detalle: {e.__str__()}"
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=jsonable_encoder(ErrorResponse(details=details)),
        )
