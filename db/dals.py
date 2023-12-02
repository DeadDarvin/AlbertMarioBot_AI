from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
