from fastapi import FastAPI,status
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title: str

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None

class CategorySchema(BaseModel):
    id: str
    name: str

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str | None = None

class BookSchema(BaseModel):
    book:str

book = ''

tasks: list[TaskSchema] = []
categories: list[CategorySchema] = []



@app.get("/tasks")
def read_root():
    return tasks


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()),title = payload.title,completed =False)
    tasks.append(new_task)
    return new_task

@app.patch('/tasks/{task_id}')
def update_task(task_id: str,payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed

            return tasks

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task( task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)

@app.get('/categories')
def read_categories():
    return categories

@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema)->CategorySchema:
    new_category = CategorySchema(id=str(uuid4()),name = payload.name)
    categories.append(new_category)
    return new_category

@app.patch('/categories/{category_id}')
def update_category(category_id: str,payload: CategoryUpdateSchema):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name
            return categories

@app.delete('/categories/{category_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)

# @app.get("/book")
# def read_root():
#     return {f'message:Любимая книга: {book}'}

# @app.post('/book')
# def get_book(payload:BookSchema):
#     global book
#     book = payload.book
#     return book




