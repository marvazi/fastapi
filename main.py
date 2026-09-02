from fastapi import FastAPI,status,Depends
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine,String,Boolean,select
from sqlalchemy.orm import sessionmaker,Session,mapped_column,Mapped,DeclarativeBase
from contextlib import asynccontextmanager

"""Проверка"""

DATABASE_URL = "postgresql+psycopg://postgres:admin@localhost:15432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker[Session](bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String, primary_key=True,default=lambda: str(uuid4()))



class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str] = mapped_column(String, index=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

class CategoryORM(Base):
    __tablename__ = "categories"
    name: Mapped[str] = mapped_column(String, index=True)

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

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



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def tasks_to_orm(task: TaskSchema) -> TaskORM:
    return TaskORM(id=task.id,title=task.title,completed=task.completed)

def categories_to_orm(category: CategorySchema) -> CategoryORM:
    return CategoryORM(id=category.id,name=category.name)

@app.get("/tasks")
def read_root(db: Session = Depends(get_db)):
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [tasks_to_orm(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema,db: Session = Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title = payload.title,completed =False)
    db.add(new_task)
    db.commit()
    return tasks_to_orm(new_task)

@app.patch('/tasks/{task_id}')
def update_task(task_id: str,payload: TaskUpdateSchema,db: Session = Depends(get_db)):
    task_update = db.get(TaskORM,task_id)
    if payload.title:
        task_update.title = payload.title
    if payload.completed is not None:
        task_update.completed = payload.completed
    db.commit()
    return task_update


@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task( task_id: str,db: Session = Depends(get_db)):
    task_delete = db.get(TaskORM,task_id)
    db.delete(task_delete)
    db.commit()
    return task_delete

@app.get('/categories')
def read_categories(db: Session = Depends(get_db)):
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [categories_to_orm(category) for category in categories_from_db]

@app.post('/categories', status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema,db: Session = Depends(get_db))->CategorySchema:
    new_category = CategoryORM(name = payload.name)
    db.add(new_category)
    db.commit()
    return categories_to_orm(new_category)

@app.patch('/categories/{category_id}')
def update_category(category_id: str,payload: CategoryUpdateSchema,db: Session = Depends(get_db)):
    category_update = db.get(CategoryORM,category_id)
    if payload.name:
        category_update.name = payload.name
    db.commit()
    return category_update
        

@app.delete('/categories/{category_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str,db: Session = Depends(get_db)):
    category_delete = db.get(CategoryORM,category_id)
    db.delete(category_delete)
    db.commit()
    return category_delete





