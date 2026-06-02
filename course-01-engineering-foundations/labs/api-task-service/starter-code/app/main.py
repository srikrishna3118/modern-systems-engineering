from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    priority: int = Field(default=3, ge=1, le=5)


class Task(BaseModel):
    id: str
    title: str
    priority: int
    status: Literal["open", "done"]
    created_at: str


class TaskList(BaseModel):
    items: list[Task]
    next_cursor: str | None


app = FastAPI(title="API Task Service")

# Starter implementation: in-memory store.
# TODO (exercise): add persistence (SQLite) and cursor pagination.
_tasks: dict[str, Task] = {}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    task_id = uuid4().hex
    task = Task(
        id=task_id,
        title=payload.title,
        priority=payload.priority,
        status="open",
        created_at=datetime.utcnow().isoformat() + "Z",
    )
    _tasks[task_id] = task
    return task


@app.get("/tasks", response_model=TaskList)
def list_tasks(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> TaskList:
    # Starter pagination: offset-based.
    # TODO (exercise): replace with cursor pagination.
    all_items = sorted(_tasks.values(), key=lambda t: t.created_at)
    page = all_items[offset : offset + limit]
    next_cursor = None
    return TaskList(items=page, next_cursor=next_cursor)


@app.post("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: str) -> Task:
    task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task_not_found")
    updated = task.model_copy(update={"status": "done"})
    _tasks[task_id] = updated
    return updated
