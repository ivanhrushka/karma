from aiohttp import web

from src.controllers.index import handler

PORT: int = 8880

app = web.Application()
app.router.add_get('/', handler)

web.run_app(app, host='localhost', port=PORT)