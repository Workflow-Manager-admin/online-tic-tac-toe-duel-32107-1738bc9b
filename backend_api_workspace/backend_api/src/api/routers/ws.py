from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
from ..game_engine import get_game

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    # PUBLIC_INTERFACE
    async def connect(self, game_id: str, websocket: WebSocket):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)

    # PUBLIC_INTERFACE
    def disconnect(self, game_id: str, websocket: WebSocket):
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]

    # PUBLIC_INTERFACE
    async def broadcast(self, game_id: str, data):
        if game_id in self.active_connections:
            for conn in self.active_connections[game_id]:
                await conn.send_json(data)


manager = ConnectionManager()


# PUBLIC_INTERFACE
@router.websocket("/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """
    WebSocket for subscribing to real-time updates for a given game.
    Send nothing—just receive broadcasts when game state changes (on moves, join, win, etc).
    """
    await manager.connect(game_id, websocket)
    try:
        while True:
            # Await a message, but we expect only pings or disconnects from client.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(game_id, websocket)


# To be called by game logic when a state change occurs to broadcast to all listeners
async def notify_game_update(game_id: str):
    game = get_game(game_id)
    if game:
        await manager.broadcast(game_id, data=game.model_dump())
