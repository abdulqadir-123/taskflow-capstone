from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select

from .database import Base, engine, get_db
from .models import User, Project, Task
from .schemas import (
    UserCreate, UserOut, ProjectCreate, ProjectUpdate, ProjectOut,
    TaskCreate, TaskUpdate, TaskOut, QuickAddRequest
)
from .algorithms import search_tasks, merge_sort, task_statistics, benchmark
from .ai_parser import parse_quick_add

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"name": "TaskFlow", "status": "running", "docs": "/docs"}

@app.post("/users", response_model=UserOut)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(409, "Email already exists")
    obj = User(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return list(db.scalars(select(User).order_by(User.id)).all())

@app.post("/projects", response_model=ProjectOut)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    if not db.get(User, data.owner_id):
        raise HTTPException(404, "Owner not found")
    obj = Project(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/projects", response_model=list[ProjectOut])
def list_projects(owner_id: int | None = None, db: Session = Depends(get_db)):
    q = select(Project).order_by(Project.id)
    if owner_id is not None:
        q = q.where(Project.owner_id == owner_id)
    return list(db.scalars(q).all())

@app.get("/projects/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    obj = db.get(Project, project_id)
    if not obj: raise HTTPException(404, "Project not found")
    return obj

@app.put("/projects/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    obj = db.get(Project, project_id)
    if not obj: raise HTTPException(404, "Project not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    obj = db.get(Project, project_id)
    if not obj: raise HTTPException(404, "Project not found")
    db.delete(obj); db.commit()
    return {"message": "Project deleted", "id": project_id}

@app.post("/tasks", response_model=TaskOut)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(Project, data.project_id):
        raise HTTPException(404, "Project not found")
    obj = Task(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(
    project_id: int | None = None,
    status: str | None = None,
    priority: str | None = None,
    sort: str = Query("id", pattern="^(id|title|priority|due_date)$"),
    db: Session = Depends(get_db)
):
    q = select(Task)
    if project_id is not None: q = q.where(Task.project_id == project_id)
    if status is not None: q = q.where(Task.status == status)
    if priority is not None: q = q.where(Task.priority == priority)
    tasks = list(db.scalars(q).all())
    priority_rank = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    if sort == "priority":
        return merge_sort(tasks, key=lambda x: priority_rank.get(x.priority, 99))
    return merge_sort(tasks, key=lambda x: (getattr(x, sort) or ""))
@app.get("/tasks/search", response_model=list[TaskOut])
def search_endpoint(q: str, project_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Task)
    if project_id is not None: stmt = stmt.where(Task.project_id == project_id)
    return search_tasks(list(db.scalars(stmt).all()), q)
@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    obj = db.get(Task, task_id)
    if not obj: raise HTTPException(404, "Task not found")
    return obj

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    obj = db.get(Task, task_id)
    if not obj: raise HTTPException(404, "Task not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    obj = db.get(Task, task_id)
    if not obj: raise HTTPException(404, "Task not found")
    db.delete(obj); db.commit()
    return {"message": "Task deleted", "id": task_id}



@app.get("/statistics")
def statistics(project_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Task)
    if project_id is not None: stmt = stmt.where(Task.project_id == project_id)
    return task_statistics(list(db.scalars(stmt).all()))

@app.get("/algorithms/benchmark")
def algorithms_benchmark(db: Session = Depends(get_db)):
    return benchmark(list(db.scalars(select(Task)).all()))

@app.post("/quick-add", response_model=TaskOut)
def quick_add(data: QuickAddRequest, db: Session = Depends(get_db)):
    if not db.get(Project, data.project_id):
        raise HTTPException(404, "Project not found")
    parsed = parse_quick_add(data.text)
    obj = Task(
        title=parsed["title"],
        description=parsed["description"],
        status=parsed["status"],
        priority=parsed["priority"],
        due_date=parsed["due_date"],
        project_id=data.project_id,
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@app.post("/seed")
def seed(db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == "demo@taskflow.local"))
    if not user:
        user = User(name="Demo User", email="demo@taskflow.local")
        db.add(user); db.commit(); db.refresh(user)
    project = db.scalar(select(Project).where(Project.name == "Demo Project"))
    if not project:
        project = Project(name="Demo Project", description="TaskFlow demonstration project", owner_id=user.id)
        db.add(project); db.commit(); db.refresh(project)
    if not db.scalar(select(Task).where(Task.project_id == project.id)):
        for title, status, priority in [
            ("Build login page", "done", "high"),
            ("Create dashboard", "in_progress", "urgent"),
            ("Write API documentation", "todo", "medium"),
            ("Test search feature", "todo", "low"),
        ]:
            db.add(Task(title=title, status=status, priority=priority, project_id=project.id))
        db.commit()
    return {"message": "Demo data ready", "user_id": user.id, "project_id": project.id}
