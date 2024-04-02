from starlette.applications import Starlette
from starlette.routing import Mount

from main.urls import routes as main_routes
from chat.urls import routes as chat_routes
from cron import one_minute_message

routes = [
    Mount("/chat", routes=chat_routes),
    Mount("/", routes=main_routes),
]


class AmqpHttpServer(Starlette):
    def __init__(self, *args, **kwargs):
        one_minute_message.start()
        super().__init__(*args, **kwargs)

# app = Starlette(routes=routes, debug=True)
app = AmqpHttpServer(routes=routes, debug=True)