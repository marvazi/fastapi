from fastapi import APIRouter
from fastapi.params import Depends
from fastapi import status
from app.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema

from app.api.dependencies import get_categories_service
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get('')
def read_categories(category_service:CategoryService = Depends(get_categories_service)):
    return category_service.list_categories()


@router.post('', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema,category_service:CategoryService = Depends(get_categories_service)) -> CategorySchema:
    return category_service.create_category(category_create=payload)


@router.patch('/{category_id}')
def update_category(category_id: str, payload: CategoryUpdateSchema, category_service:CategoryService = Depends(get_categories_service)):
    return category_service.update_category(category_id=category_id, category_update=payload)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_service:CategoryService = Depends(get_categories_service)):
    return category_service.delete_task(category_id=category_id)