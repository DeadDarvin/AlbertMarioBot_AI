from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Person
from db.models import User


class UserDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, telegram_id: int) -> User | None:
        query = select(User).where(User.telegram_id == telegram_id)
        user_by_id = await self.session.scalar(query)
        return user_by_id

    async def register_new_user(
        self,
        telegram_id: int,
        username: str | None,
        name: str | None,
        surname: str | None,
    ) -> None:
        new_user = User(
            telegram_id=telegram_id, username=username, name=name, surname=surname
        )
        self.session.add(new_user)
        await self.session.flush()

    async def update_user_companion(self, telegram_id: int, companion_id: int):
        query = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(current_person_id=companion_id)
        )
        await self.session.execute(query)


class PersonDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_person_by_id(self, person_id: int) -> Person | None:
        query = select(Person).where(Person.id == person_id)
        return await self.session.scalar(query)
