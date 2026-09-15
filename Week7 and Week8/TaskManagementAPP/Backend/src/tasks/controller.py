from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.tasks.dtos import TaskSchema, TaskUpdateSchema
from src.tasks.models import TaskModel
from src.user.models import UserModel

def create_task(body: TaskSchema, db: Session , user:UserModel):
    data = body.model_dump()

    new_task = TaskModel(**data,
                        user_id = user.id )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks(db: Session ,user:UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user.id).all()

    return tasks


def get_one_task(task_id: int, db: Session , user:UserModel):
    one_task = (
        db.query(TaskModel)
        .filter(
            TaskModel.id == task_id,
            TaskModel.user_id == user.id
        )
        .first()
    )

    if not one_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return one_task


def update_task(
    body: TaskUpdateSchema,
    task_id: int,
    db: Session,
    user:UserModel
):
    one_task:TaskModel = db.get(TaskModel, task_id)

    if not one_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if one_task.user_id != user.id:
        raise HTTPException(403,detail="You are not allowed to update")
    data = body.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(one_task, field, value)

    db.commit()
    db.refresh(one_task)

    return one_task


def delete_task(task_id: int, db: Session,user:UserModel):
    one_task = db.get(TaskModel, task_id)
    if one_task.user_id != user.id:
        raise HTTPException(403,detail="You are not allowed to Delete")

    if not one_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(one_task)
    db.commit()

    return None