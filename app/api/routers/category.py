from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_categories_service
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])

CategoryServiceDep = Annotated[
    CategoryService,
    Depends(get_categories_service),
]


@router.get("")
def read_categories(
    category_service: CategoryServiceDep,
) -> list[CategorySchema]:
    return category_service.list_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryServiceDep,
) -> CategorySchema:
    return category_service.create_category(category_create=payload)


@router.patch("/{category_id}")
def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    category_service: CategoryServiceDep,
) -> CategorySchema:
    return category_service.update_category(
        category_id=category_id,
        category_update=payload,
    )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: str,
    category_service: CategoryServiceDep,
) -> None:
    category_service.delete_category(category_id=category_id)
