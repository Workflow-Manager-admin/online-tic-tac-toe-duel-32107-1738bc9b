from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class PlayerMark(str, Enum):
    PLAYER_X = "X"
    PLAYER_O = "O"


# PUBLIC_INTERFACE
class User(BaseModel):
    """A user account or guest."""

    user_id: str = Field(..., description="Unique user identifier")
    name: str = Field(..., description="Display name")
    is_guest: bool = Field(..., description="True if this is a guest user")


# PUBLIC_INTERFACE
class GuestLoginRequest(BaseModel):
    """Request payload to login as guest."""

    name: str = Field(..., description="Guest display name (optional)", max_length=32)


# PUBLIC_INTERFACE
class LoginResponse(BaseModel):
    """Token and user details on login/guest access."""

    user: User
    token: str


# PUBLIC_INTERFACE
class GameCreateRequest(BaseModel):
    """Request to create a new Tic Tac Toe game."""

    user_id: str = Field(..., description="ID of user creating game")


# PUBLIC_INTERFACE
class GameJoinRequest(BaseModel):
    """Request to join an existing game."""

    user_id: str = Field(..., description="User joining")
    game_id: str = Field(..., description="Game ID")


# PUBLIC_INTERFACE
class MoveRequest(BaseModel):
    """Request representing a Tic Tac Toe move."""

    user_id: str = Field(..., description="Player ID")
    row: int = Field(..., ge=0, le=2, description="Row of move (0-2)")
    col: int = Field(..., ge=0, le=2, description="Column of move (0-2)")
    game_id: str = Field(..., description="Game ID")


# Board represented as 3x3 array
Board = List[List[Optional[PlayerMark]]]


class GameStatus(str, Enum):
    WAITING = "waiting"
    ACTIVE = "active"
    DONE = "done"


# PUBLIC_INTERFACE
class Game(BaseModel):
    """Game object, as returned from REST APIs."""

    game_id: str = Field(..., description="Unique game identifier")
    owner_id: str = Field(..., description="User who created the game")
    player_x: Optional[User] = Field(None, description="Player X info, if joined")
    player_o: Optional[User] = Field(None, description="Player O info, if joined")
    board: Board = Field(..., description="3x3 tic-tac-toe board")
    turn: PlayerMark = Field(
        ..., description='"X" or "O" - which player\'s turn'
    )
    status: GameStatus = Field(..., description="waiting/active/done")
    winner: Optional[PlayerMark] = Field(
        None, description='"X" or "O" if there\'s a winner'
    )
    draw: bool = Field(False, description="True if the game ended in a draw")
    created_at: Optional[str] = Field(
        None, description="Creation timestamp ISO8601"
    )
    updated_at: Optional[str] = Field(
        None, description="Last updated ISO8601 (for clients to poll/refresh)"
    )
