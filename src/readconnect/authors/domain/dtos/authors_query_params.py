from readconnect.shared.domain.dtos.query_params import QueryParams


class AuthorsQueryParams(QueryParams):
    include_books: bool = False
