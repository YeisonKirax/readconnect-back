from readconnect.users.domain.models.user_model import User


async def create_user(name: str, surname: str) -> User:
    user = User(name=name, surname=surname)
    return user
