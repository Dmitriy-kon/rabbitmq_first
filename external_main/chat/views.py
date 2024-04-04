import json


from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from connection_manager import ConectionManager
from .html import html

from producer import methods as p_methods


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
            data_json = json.loads(data)
            await manager.register_user(websocket, data_json["username"])

            # await manager.send_personal_message(f"Message text was: {data}", websocket)
            await p_methods.send_message_to_queue(data_json)
            await manager.send_json(data_json, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client disconnected: {websocket}")
