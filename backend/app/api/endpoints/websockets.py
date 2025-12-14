from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # Map lot_id -> list of websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, lot_id: str):
        await websocket.accept()
        if lot_id not in self.active_connections:
            self.active_connections[lot_id] = []
        self.active_connections[lot_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lot_id: str):
        if lot_id in self.active_connections:
            self.active_connections[lot_id].remove(websocket)

    async def broadcast(self, message: dict, lot_id: str):
        if lot_id in self.active_connections:
            for connection in self.active_connections[lot_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/lot/{lot_id}")
async def websocket_endpoint(websocket: WebSocket, lot_id: str):
    await manager.connect(websocket, lot_id)
    try:
        while True:
            # Just keep connection open, we primarily push TO client
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, lot_id)
