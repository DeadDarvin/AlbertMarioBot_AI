from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import REAL_DATABASE_URL

##############################################
# BLOCK FOR COMMON INTERACTION WITH DATABASE #
##############################################


# create async engine for interaction with database
engine = create_async_engine(REAL_DATABASE_URL, future=True, echo=False)

# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def into_new_async_session(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        session: AsyncSession = async_session()
        try:
            await function(session, *args, **kwargs)
        finally:
            await session.close()

    return wrapper
