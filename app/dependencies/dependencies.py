from fastapi import Query

from app.schema.publication_schema import Pagination


def pagination_params(
        page: int = Query(ge=1, required=False, default=1, le=500000),
        per_page: int = Query(ge=1, required=False, default=10, le=100)
):
    return Pagination(per_page=per_page, page=page)
