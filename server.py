from aiohttp import web

from src.routes.index import setup_routes

PORT = 8880
HOST = 'localhost'

app = web.Application()
setup_routes(app)

web.run_app(app, host=HOST, port=PORT)