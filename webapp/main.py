
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.usernames: dict = {}  # Maps WebSocket to username

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.usernames[websocket] = username

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            del self.usernames[websocket]

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Handle failed WebSocket sends
                self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    # Each client should send its username upon connection
    await manager.broadcast(f"{username}")

    try:
        while True:
            data = await websocket.receive_text()
            # The server should prepend the username to each message before broadcasting it to other clients.
            message = f"{username}: {data}"
            # When a message is received from a client, broadcast this message to all connected clients.
            await manager.broadcast(message)
    except WebSocketDisconnect:
        # Handle client disconnections gracefully and remove their WebSocket connections from the active connections list
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} has left the chat.")