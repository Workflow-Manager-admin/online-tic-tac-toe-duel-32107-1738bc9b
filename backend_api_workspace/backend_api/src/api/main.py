from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, game, ws


app = FastAPI(
    title="Online Tic Tac Toe Duel API",
    description=(
        "FastAPI backend for real-time Tic Tac Toe games between two online players, "
        "featuring authentication, REST game state endpoints, and WebSocket live updates."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "User login and guest authentication"},
        {"name": "game", "description": "Game creation, joining, state, and moves"},
        {"name": "ws", "description": "Real-time game updates via WebSocket"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check
@app.get("/", tags=["status"])
def health_check():
    """Check if service is running."""
    return {"message": "Healthy"}


# Register routers for versioned API endpoint paths
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(game.router, prefix="/api/game", tags=["game"])
app.include_router(ws.router, prefix="/api/ws", tags=["ws"])
