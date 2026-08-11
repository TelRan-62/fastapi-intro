from fastapi import FastAPI, HTTPException

from task_model import Task, TaskDTO

app = FastAPI()

tasks_db = []


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/tasks")
def get_tasks(skip: int = 0, limit: int = 10):
    return tasks_db[skip:skip + limit]


@app.post("/tasks")
def create_task(task_dto: TaskDTO):
    task = Task(title=task_dto.title, description=task_dto.description, id=len(tasks_db))
    tasks_db.append(task)
    return task