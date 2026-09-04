from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        category_orm = self.category_repository.get_all()

        return [CategorySchema.model_validate(category) for category in category_orm]

    def create_category(
        self,
        category_create: CategoryCreateSchema,
    ) -> CategorySchema:
        category_orm = self.category_repository.create(name=category_create.name)

        self.db.commit()
        self.db.refresh(category_orm)

        return CategorySchema.model_validate(category_orm)

    def update_category(
        self,
        category_id: str,
        category_update: CategoryUpdateSchema,
    ) -> CategorySchema:
        category_for_update = self.category_repository.get_by_id(
            category_id=category_id
        )

        if category_for_update is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        if category_update.name is not None:
            category_for_update.name = category_update.name

        self.db.commit()
        self.db.refresh(category_for_update)

        return CategorySchema.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        category_orm = self.category_repository.get_by_id(category_id=category_id)

        if category_orm is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        self.category_repository.delete(category_orm)
        self.db.commit()
