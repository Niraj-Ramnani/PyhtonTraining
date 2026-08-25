from fastapi import APIRouter
from src.tasks import controller

task_routes = APIRouter(prefix="/tasks")

@task_routes.post("/create")
def create_task():
    return controller.cretate_task()
