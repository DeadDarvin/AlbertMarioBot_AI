from envparse import Env

from dev_secrets import AMPLITUDE_API_KEY
from dev_secrets import BOT_TOKEN
from dev_secrets import GPT_API_URL

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


####################
# API DATA
####################
GPT_API_URL = env.str("GPT_API_URL", default=GPT_API_URL)
AMPLITUDE_API_KEY = env.str("AMPLITUDE_API_KEY", default=AMPLITUDE_API_KEY)
