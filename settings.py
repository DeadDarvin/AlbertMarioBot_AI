from envparse import Env

from dev_secrets import BOT_TOKEN

env = Env()

####################
# BOT DATA
####################
BOT_TOKEN = env.str("BOT_TOKEN", default=BOT_TOKEN)


####################
# DATABASE DATA
####################
REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5444/postgres",
)
