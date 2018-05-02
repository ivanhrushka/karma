from aiohttp import web
import jwt


JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS: 20


async def handle_404(request, response):
    response = web.json_response({'error': '404'})
    return response


async def handle_500(request, response):
    response = web.json_response({'error': '500'})
    return response


def http_error(overrides):
    @web.middleware
    async def middleware(request, handler):
        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override is None:
                return response
            else:
                return await override(request, response)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override is None:
                raise
            else:
                return await override(request, ex)
    return middleware


async def auth_middleware(app, handler):
    @web.middleware
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET,
                                     algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return web.json_response({'error': 'Token is invalid'}, status=400)
            
            request.user = User.objects.get(id=payload['user_id'])

        return await handler(request)
    return middleware


def setup_middlewares(app):
    error_middleware = http_error({404: handle_404,
                                    500: handle_500})
    app.middlewares.append(error_middleware)
    app.middlewares.append(auth_middleware)
