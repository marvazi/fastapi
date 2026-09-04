from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_task_service
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

TaskServiceDep = Annotated[
    TaskService,
    Depends(get_task_service),
]


@router.get("")
def read_tasks(
    task_service: TaskServiceDep,
) -> list[TaskSchema]:
    return task_service.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema,
    task_service: TaskServiceDep,
) -> TaskSchema:
    return task_service.create_task(task_create=payload)


@router.patch("/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    task_service: TaskServiceDep,
) -> TaskSchema:
    return task_service.update_task(
        task_id=task_id,
        task_update=payload,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: str,
    task_service: TaskServiceDep,
) -> None:
    task_service.delete_task(task_id=task_id)
