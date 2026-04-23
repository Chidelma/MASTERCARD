from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from python_api.db.database import SessionDep
from python_api.db.schemas import Task
from python_api.models import CreateTask, TaskResponse


router = APIRouter(prefix="/tasks", tags=["tasks"])


def _get_active_tasks_for_user(db: SessionDep, user_id: int) -> list[TaskResponse]:
    rows = db.query(Task).filter(Task.user_id == user_id, Task.deleted.is_(False)).all()
    return [TaskResponse.model_validate(row) for row in rows]

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


@router.get("", status_code=status.HTTP_200_OK)
def get_my_tasks(riskrecon_user_id: Annotated[int, Header()], db: SessionDep) -> list[TaskResponse]:
    try:
        return _get_active_tasks_for_user(db, riskrecon_user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get tasks for the authenticated user",
        ) from e


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user_tasks(user_id: int, riskrecon_user_id: Annotated[int, Header()], db: SessionDep) -> list[TaskResponse]:
    if user_id != riskrecon_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Users may only access their own tasks",
        )

    try:
        return _get_active_tasks_for_user(db, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get tasks for {user_id}",
        ) from e
