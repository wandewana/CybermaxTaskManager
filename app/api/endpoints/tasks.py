from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db import crud
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.api import deps
from app.models.user import User

router = APIRouter()


from fastapi import status

@router.post(
    "/",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the current user.",
    tags=["tasks"]
)
async def create_task(
    *, 
    db: AsyncSession = Depends(deps.get_db),
    task_in: TaskCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Task:
    """
    Create a new task for the current user.
    """
    task = await crud.create_task(db, task_in=task_in, owner_id=current_user.id)
    return task


@router.get(
    "/",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
    summary="List tasks",
    description="Retrieve all tasks for the current user. Optionally filter by completion status.",
    tags=["tasks"]
)
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    is_completed: Optional[bool] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[Task]:
    """
    Retrieve tasks for the current user.
    """
    tasks = await crud.get_tasks(
        db, owner_id=current_user.id, is_completed=is_completed
    )
    return tasks


@router.put(
    "/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update a task by ID for the current user.",
    tags=["tasks"]
)
async def update_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Task:
    """
    Update a task by ID for the current user.
    """
    db_task = await crud.get_task(db, id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task = await crud.update_task(db=db, db_task=db_task, task_in=task_in)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> None:
    """
    Delete a task.
    """
    db_task = await crud.get_task(db, id=task_id)
    if not db_task:
        # Even if the task doesn't exist, we don't want to reveal that
        # to a potential attacker. So we can pretend it was deleted.
        return
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    await crud.delete_task(db=db, db_task=db_task)
    return
