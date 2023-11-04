import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from ...application.login_user.login_user_use_case import LoginUserUseCase
from ...application.signup_user.signup_user_use_case import SignupUserUseCase
from ...domain.dtos.login_request_dto import LoginRequestDTO
from ...domain.dtos.login_response_dto import LoginResponseDTO
from ...domain.dtos.signup_request_dto import SignupRequestDTO

auth_router = APIRouter(prefix="/auth")


@auth_router.post(path="/login", status_code=200)
async def login(
    body: LoginRequestDTO,
    login_use_case: Annotated[LoginUserUseCase, Depends(LoginUserUseCase)],
) -> LoginResponseDTO:
    logging.info(body)
    response = await login_use_case.execute(body)
    return response


@auth_router.post(path="/signup", status_code=200)
async def signup(
    body: SignupRequestDTO,
    signup_use_case: Annotated[SignupUserUseCase, Depends(SignupUserUseCase)],
) -> LoginResponseDTO:
    logging.info(body)
    response = await signup_use_case.execute(body)
    return response
