from fastapi import APIRouter, Depends, HTTPException

from loggers.logger_req import logger
from models.task_model import TaskDTO, Task

router = APIRouter(prefix="/tasks")

tasks_db = [Task(title="Task 1", description="Description 1", id=0),
            Task(title="Task 2", description="Description 2", id=1)]

def pagination_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@router.get("/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.get("/")
def get_tasks(pagination: dict = Depends(pagination_params)):
    return tasks_db[pagination["skip"]:pagination["skip"] + pagination["limit"]]


@router.post("/")
def create_task(task_dto: TaskDTO):
    logger.debug(f"Creating task: {task_dto.title} - {task_dto.description}")
    task = Task(title=task_dto.title, description=task_dto.description, id=len(tasks_db))
    tasks_db.append(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int):
    for idx, task in enumerate(tasks_db):
        if task.id == task_id:
            del tasks_db[idx]
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}")
def update_task(task_id: int, task_dto: TaskDTO):
    for idx, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[idx] = Task(title=task_dto.title, description=task_dto.description, id=task_id)
            return tasks_db[idx]
    raise HTTPException(status_code=404, detail="Task not found")
