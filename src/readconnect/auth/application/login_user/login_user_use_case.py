from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.auth.domain.dtos.login_request_dto import LoginRequestDTO
from readconnect.auth.domain.dtos.login_response_dto import LoginResponseDTO
from readconnect.auth.domain.services.auth_service import AuthService


@dataclass()
class LoginUserUseCase:
    auth_service: Annotated[AuthService, Depends(AuthService)]

    async def execute(self, request: LoginRequestDTO) -> LoginResponseDTO:
        user_found = self.auth_service.get_user_by_email(request.email)
        if user_found is None:
            raise Exception("error usuario no encontrado")
        is_valid_pass = self.auth_service.verify_password(
            request.password, user_found.password
        )
        if not is_valid_pass:
            raise Exception("error")

        token = self.auth_service.generate_jwt(
            {
                "id": user_found.id,
                "email": user_found.email,
                "name": user_found.name,
                "surname": user_found.surname,
            }
        )
        return LoginResponseDTO(token=token)
