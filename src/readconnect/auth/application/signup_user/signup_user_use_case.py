from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from readconnect.auth.domain.dtos.signup_request_dto import SignupRequestDTO
from readconnect.auth.domain.dtos.signup_response_dto import SignupResponseDTO
from readconnect.auth.domain.services.auth_service import AuthService
from readconnect.users.domain.models.user_model import User


@dataclass()
class SignupUserUseCase:
    auth_service: Annotated[AuthService, Depends(AuthService)]

    async def execute(self, request: SignupRequestDTO) -> SignupResponseDTO:
        user_found = await self.auth_service.get_user_by_email(request.email)
        if user_found is not None:
            raise Exception("error usuario ya existe")

        password_hash = self.auth_service.get_password_hash(request.password)
        user_model = User(
            name=request.name,
            surname=request.surname,
            email=request.email,
            password=password_hash,
        )
        user_created = await self.auth_service.create_new_user(user_model)
        token = self.auth_service.generate_jwt(
            {
                "id": user_created.id,
                "email": user_created.email,
                "name": user_created.name,
                "surname": user_created.surname,
            }
        )
        return SignupResponseDTO(token=token)
