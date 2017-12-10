from aiohttp import web

async def handler(request):
    data: dict = {
        'text': 'Server is working now',
        'request_method': request.method
    }
    return web.json_response(data)