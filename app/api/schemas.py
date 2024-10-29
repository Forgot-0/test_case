from typing import Generic, TypeVar

from pydantic import BaseModel


TListItem = TypeVar("TListItem")


class PaginationOutSchema(BaseModel):
    page: int
    limit: int
    total: int


class ListPaginatedResponse(BaseModel, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOutSchema
