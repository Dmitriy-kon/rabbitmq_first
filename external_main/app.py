from starlette.applications import Starlette
from starlette.routing import Mount

from main.urls import routes as main_routes

routes = [
    Mount("/", routes=main_routes),
]


class AmqpHttpServer(Starlette):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

app = AmqpHttpServer(routes=routes)