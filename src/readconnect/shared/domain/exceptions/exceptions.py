import dataclasses


@dataclasses.dataclass()
class NotFoundError(Exception):
    details: str
    status_code: int


@dataclasses.dataclass()
class InvalidsCredentialsError(Exception):
    details: str
    status_code: int
