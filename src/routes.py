import pathlib

from .views import index, signup


PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', index)

    app.router.add_post('/api/auth/signup', signup)
    app.router.add_post('/api/auth/login', index)

    app.router.add_post('/api/auth/karma', index)
    app.router.add_patch('/api/auth/karma/up', index)
    app.router.add_patch('/api/auth/karma/down', index)
    