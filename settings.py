from envparse import Env

from dev_secrets import BOT_TOKEN

env = Env()

####################
# BOT DATA
####################
BOT_TOKEN = env.str("BOT_TOKEN", default=BOT_TOKEN)
