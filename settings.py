from envparse import Env

env = Env()

####################
# BOT DATA
####################
BOT_TOKEN = env.str("BOT_TOKEN")
WEB_APP_URL = env.str(
    "WEB_APP_URL",
    default="https://deaddarvin.github.io/AlbertMarioBot_AI/web_app/web_app.html",
)

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
GPT_API_URL = env.str("GPT_API_URL")
AMPLITUDE_API_KEY = env.str("AMPLITUDE_API_KEY")
