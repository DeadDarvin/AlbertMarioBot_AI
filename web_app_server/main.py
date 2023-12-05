"""
Server-module for getting data from WebAppTelegram.
"""
import aiohttp_cors
from aiohttp import web

from web_app_server.routes import routes

app = web.Application()


app.add_routes(routes)
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*"
        )
    },
)
for route in list(app.router.routes()):
    cors.add(route)


if __name__ == "__main__":
    web.run_app(app=app, host="0.0.0.0", port=8000)
