from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserCreate
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, *, user_id: int) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, *, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_task(db: AsyncSession, *, task_in: TaskCreate, owner_id: int) -> Task:
    db_task = Task(**task_in.dict(), owner_id=owner_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_tasks(
    db: AsyncSession, *, owner_id: int, is_completed: Optional[bool] = None
) -> List[Task]:
    query = select(Task).filter(Task.owner_id == owner_id)
    if is_completed is not None:
        query = query.filter(Task.is_completed == is_completed)
    result = await db.execute(query.order_by(Task.id))
    return result.scalars().all()


async def get_task(db: AsyncSession, *, id: int) -> Optional[Task]:
    result = await db.execute(select(Task).filter(Task.id == id))
    return result.scalars().first()


async def update_task(
    db: AsyncSession, *, db_task: Task, task_in: TaskUpdate
) -> Task:
    update_data = task_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_task, field, update_data[field])
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, *, db_task: Task) -> None:
    await db.delete(db_task)
    await db.commit()
