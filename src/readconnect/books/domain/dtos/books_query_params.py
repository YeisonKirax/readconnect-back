from shared.domain.dtos.query_params import QueryParams


class BooksQueryParams(QueryParams):
    include_extra_data: bool = False
