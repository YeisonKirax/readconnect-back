import dataclasses


@dataclasses.dataclass()
class ErrorResponse:
    status: str = "error"
    details: str = ""
