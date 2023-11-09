from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, status

from readconnect.auth.domain.dtos.signup_request_dto import SignupRequestDTO
from readconnect.auth.domain.dtos.signup_response_dto import SignupResponseDTO
from readconnect.auth.domain.services.auth_service import AuthService
from readconnect.shared.domain.exceptions.exceptions import InvalidsCredentialsError
from readconnect.users.domain.models.user_model import User


@dataclass()
class SignupUserUseCase:
    auth_service: Annotated[AuthService, Depends(AuthService)]

    async def execute(self, request: SignupRequestDTO) -> SignupResponseDTO:
        user_found = await self.auth_service.get_user_by_email(request.email)
        if user_found is not None:
            raise InvalidsCredentialsError(
                details="ya existe un correo registrado",
                status_code=status.HTTP_409_CONFLICT,
            )

        password_hash = self.auth_service.get_password_hash(request.password)
        user_model = User(
            name=request.name,
            surname=request.surname,
            email=request.email,
            password=password_hash,
        )
        await self.auth_service.create_new_user(user_model)

        return SignupResponseDTO(status="ok", message="registrado correctamente")
