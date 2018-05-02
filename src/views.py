from aiohttp import web

from . import db


def login_required(func):
    def wrapper(request):
        if not request.user:
            return web.json_response({'error': 'Auth required'}, status=401)
        return func(request)
    return wrapper

@login_required
async def index(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.karma.select())
        records = await cursor.fetchall()
        questions = [dict(q) for q in records]
        return web.json_response(questions)
