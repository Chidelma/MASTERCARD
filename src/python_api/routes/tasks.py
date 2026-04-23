from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from python_api.db.database import SessionDep
from python_api.db.schemas import Task
from python_api.models import CreateTask, TaskResponse, TaskRec


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(task: CreateTask, riskrecon_user_id: Annotated[int, Header()], db: SessionDep) -> TaskResponse:
    db_task = Task(
        user_id = riskrecon_user_id,
        name=task.name,
        description=task.description,
        due_date=task.due_date,
    )

    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        ) from e

    return TaskResponse.model_validate(db_task)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_tasks(user_id: str,  db: SessionDep) -> list[TaskRec]:

    tasks: list[TaskRec] = []

    try:

        rows = db.query(Task).filter(Task.user_id==int(user_id), Task.deleted==False).all()

        for row in rows:
            tasks.append(TaskRec.model_validate(row))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task for {user_id}",
        ) from e
    
    return tasks