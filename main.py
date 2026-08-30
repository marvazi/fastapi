from fastapi import FastAPI
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

class BookSchema(BaseModel):
    book:str

book = ''

tasks: list[TaskSchema] = []



@app.get("/tasks")
def read_root():
    return tasks


@app.post("/tasks")
def create_task(payload: TaskCreateSchema) -> TaskSchema:
    new_task = TaskSchema(id=str(uuid4()),title = payload.title,completed =False)
    tasks.append(new_task)
    return new_task

@app.get("/book")
def read_root():
    return {f'message:Любимая книга: {book}'}

@app.post('/book')
def get_book(payload:BookSchema):
    global book 
    book = payload.book
    return book




