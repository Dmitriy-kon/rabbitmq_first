import json


from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse, JSONResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from .connection_manager import ConectionManager
from .html import html


manager = ConectionManager()


async def chat_page(request):
    # return JSONResponse({"hello": "world"})
    return HTMLResponse(html)


# async def user_message(scope, receive, send):
#     websocket = WebSocket(scope=scope, receive=receive, send=send)
async def user_message(websocket: WebSocket):
    await manager.connect(websocket)
    await manager.send_personal_message("Hello from server!", websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)

            # await manager.send_personal_message(f"Message text was: {data}", websocket)
            await manager.send_json(data, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client disconnected: {websocket}")
