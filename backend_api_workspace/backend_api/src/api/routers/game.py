from fastapi import APIRouter, HTTPException
from ..models import GameCreateRequest, GameJoinRequest, MoveRequest, Game
from ..game_engine import (
    get_user,
    create_game,
    join_game,
    get_game,
    list_open_games,
    make_move,
    get_games_for_user,
)

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/create",
    response_model=Game,
    summary="Create Game",
    description="Start a new Tic Tac Toe game (waiting for second player).",
)
async def create_game_endpoint(payload: GameCreateRequest):
    user = get_user(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    game = create_game(user)
    return game


# PUBLIC_INTERFACE
@router.post(
    "/join",
    response_model=Game,
    summary="Join Game",
    description="Join an existing Tic Tac Toe game.",
)
async def join_game_endpoint(payload: GameJoinRequest):
    user = get_user(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    game = join_game(user, payload.game_id)
    if not game:
        raise HTTPException(
            status_code=404, detail="Cannot join game. Already started or not found."
        )
    return game


# PUBLIC_INTERFACE
@router.get(
    "/list",
    response_model=list[Game],
    summary="List Waiting Games",
    description="Get games that are waiting for a second player.",
)
async def list_games():
    return list_open_games()


# PUBLIC_INTERFACE
@router.get(
    "/{game_id}",
    response_model=Game,
    summary="Get Game State",
    description="Get board, status, and players for a game.",
)
async def get_game_state(game_id: str):
    game = get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


# PUBLIC_INTERFACE
@router.post(
    "/move",
    response_model=Game,
    summary="Submit Move",
    description="Submit a move for your turn.",
)
async def submit_move(payload: MoveRequest):
    user = get_user(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    game = make_move(user, payload.game_id, payload.row, payload.col)
    if not game:
        raise HTTPException(status_code=400, detail="Invalid move or game not found.")
    return game


# PUBLIC_INTERFACE
@router.get(
    "/user/{user_id}",
    response_model=list[Game],
    summary="List User Games",
    description="Get list of games user is in.",
)
async def get_user_games(user_id: str):
    return get_games_for_user(user_id)
