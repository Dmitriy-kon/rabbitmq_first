from starlette.websockets import WebSocket

class ConectionManager:
    def __init__(self) -> None:
        self.active_connections: set[WebSocket] = set()
        self.users = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    async def register_user(self, websocket: WebSocket, name: str):
        self.users[name] = websocket
        
    def disconnect(self, websocket: WebSocket, name:str = None):
        self.active_connections.remove(websocket)
        if name:
            del self.users[name]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def send_json(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)