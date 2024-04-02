from starlette.routing import WebSocketRoute, Route

from .views import user_message, chat_page

routes = [
    Route("/", endpoint=chat_page),
    WebSocketRoute("/ws", endpoint=user_message, name="user_message"),
]