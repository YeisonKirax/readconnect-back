from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, status

from readconnect.auth.domain.dtos.login_request_dto import LoginRequestDTO
from readconnect.auth.domain.dtos.login_response_dto import LoginResponseDTO
from readconnect.auth.domain.services.auth_service import AuthService
from readconnect.shared.domain.exceptions.exceptions import InvalidsCredentialsError


@dataclass()
class LoginUserUseCase:
    auth_service: Annotated[AuthService, Depends(AuthService)]

    async def execute(self, request: LoginRequestDTO) -> LoginResponseDTO:
        user_found = await self.auth_service.get_user_by_email(request.email)
        if user_found is None:
            raise InvalidsCredentialsError(
                details="credenciales inválidas", status_code=status.HTTP_404_NOT_FOUND
            )
        is_valid_pass = self.auth_service.verify_password(
            request.password, user_found.password
        )
        if not is_valid_pass:
            raise InvalidsCredentialsError(
                details="credenciales inválidas", status_code=status.HTTP_404_NOT_FOUND
            )

        token = self.auth_service.generate_jwt(
            {
                "id": user_found.id,
                "avatar": user_found.avatar,
                "fullName": f"{user_found.name} {user_found.surname}",
            }
        )
        return LoginResponseDTO(
            token=token,
            fullName=f"{user_found.name} {user_found.surname}",
            user_id=user_found.id,
            avatar=user_found.avatar,
        )
