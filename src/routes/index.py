from ..controllers.index import handler


def setup_routes(app):
    app.router.add_get('/', handler)