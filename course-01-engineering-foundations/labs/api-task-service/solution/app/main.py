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

_tasks_in_order: list[Task] = []
_tasks_by_id: dict[str, Task] = {}


def _encode_cursor(index: int) -> str:
    return str(index)


def _decode_cursor(cursor: str | None) -> int:
    if cursor is None:
        return 0
    try:
        value = int(cursor)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="invalid_cursor") from exc
    if value < 0:
        raise HTTPException(status_code=400, detail="invalid_cursor")
    return value


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
    _tasks_in_order.append(task)
    _tasks_by_id[task_id] = task
    return task


@app.get("/tasks", response_model=TaskList)
def list_tasks(
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
) -> TaskList:
    start = _decode_cursor(cursor)
    page = _tasks_in_order[start : start + limit]
    next_cursor = None
    if start + limit < len(_tasks_in_order):
        next_cursor = _encode_cursor(start + limit)
    return TaskList(items=page, next_cursor=next_cursor)


@app.post("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: str) -> Task:
    task = _tasks_by_id.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task_not_found")
    updated = task.model_copy(update={"status": "done"})

    _tasks_by_id[task_id] = updated
    for idx, item in enumerate(_tasks_in_order):
        if item.id == task_id:
            _tasks_in_order[idx] = updated
            break

    return updated
