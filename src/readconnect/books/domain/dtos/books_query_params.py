from readconnect.shared.domain.dtos.query_params import QueryParams


class BooksQueryParams(QueryParams):
    search: str | None = None
    include_extra_data: bool = False
