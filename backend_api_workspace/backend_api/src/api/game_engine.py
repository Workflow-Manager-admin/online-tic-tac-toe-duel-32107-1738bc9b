from typing import Dict, Optional, List
from uuid import uuid4
from datetime import datetime
from .models import User, Game, GameStatus, PlayerMark


class InMemoryStore:
    """Simple in-memory store, not production ready."""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.games: Dict[str, Game] = {}


db = InMemoryStore()


# PUBLIC_INTERFACE
def create_guest_user(name: str) -> User:
    uid = str(uuid4())
    user = User(user_id=uid, name=name, is_guest=True)
    db.users[uid] = user
    return user


# PUBLIC_INTERFACE
def get_user(user_id: str) -> Optional[User]:
    return db.users.get(user_id)


# PUBLIC_INTERFACE
def create_game(owner: User) -> Game:
    game_id = str(uuid4())
    now = datetime.utcnow().isoformat()
    game = Game(
        game_id=game_id,
        owner_id=owner.user_id,
        player_x=owner,
        player_o=None,
        board=[[None, None, None], [None, None, None], [None, None, None]],
        turn=PlayerMark.PLAYER_X,
        status=GameStatus.WAITING,
        winner=None,
        draw=False,
        created_at=now,
        updated_at=now,
    )
    db.games[game_id] = game
    return game


# PUBLIC_INTERFACE
def join_game(user: User, game_id: str) -> Optional[Game]:
    game = db.games.get(game_id)
    if not game:
        return None
    if game.player_o or (game.player_x and game.player_x.user_id == user.user_id):
        return None
    game.player_o = user
    game.status = GameStatus.ACTIVE
    game.updated_at = datetime.utcnow().isoformat()
    db.games[game_id] = game
    return game


# PUBLIC_INTERFACE
def list_open_games() -> List[Game]:
    return [game for game in db.games.values() if game.status == GameStatus.WAITING]


def _is_cell_empty(board, row, col):
    return board[row][col] is None


def _check_winner(board):
    for mark in ["X", "O"]:
        # Rows, cols, diags
        for i in range(3):
            if all(cell == mark for cell in board[i]):
                return mark
            if all(board[j][i] == mark for j in range(3)):
                return mark
        if all(board[i][i] == mark for i in range(3)):
            return mark
        if all(board[i][2 - i] == mark for i in range(3)):
            return mark
    return None


# PUBLIC_INTERFACE
def make_move(user: User, game_id: str, row: int, col: int) -> Optional[Game]:
    game = db.games.get(game_id)
    if not game or game.status != GameStatus.ACTIVE:
        return None
    board = game.board
    if not _is_cell_empty(board, row, col):
        return None
    mark = PlayerMark.PLAYER_X if game.player_x.user_id == user.user_id else PlayerMark.PLAYER_O
    if game.turn != mark:
        return None
    board[row][col] = mark.value
    winner = _check_winner(board)
    if winner:
        game.status = GameStatus.DONE
        # winner will be string "X" or "O", convert to enum
        if winner == "X":
            game.winner = PlayerMark.PLAYER_X
        elif winner == "O":
            game.winner = PlayerMark.PLAYER_O
        else:
            game.winner = None
        game.draw = False
    elif all(cell is not None for row_ in board for cell in row_):
        game.status = GameStatus.DONE
        game.winner = None
        game.draw = True
    else:
        game.turn = (
            PlayerMark.PLAYER_O
            if game.turn == PlayerMark.PLAYER_X
            else PlayerMark.PLAYER_X
        )
    game.updated_at = datetime.utcnow().isoformat()
    return game


# PUBLIC_INTERFACE
def get_game(game_id: str) -> Optional[Game]:
    return db.games.get(game_id)


# PUBLIC_INTERFACE
def get_games_for_user(user_id: str):
    return [
        game
        for game in db.games.values()
        if (game.player_x and game.player_x.user_id == user_id)
        or (game.player_o and game.player_o.user_id == user_id)
    ]
