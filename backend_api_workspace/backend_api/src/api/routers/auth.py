from fastapi import APIRouter, HTTPException
from uuid import uuid4

from ..models import GuestLoginRequest, LoginResponse
from ..game_engine import create_guest_user

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/guest",
    response_model=LoginResponse,
    summary="Guest Login",
    description="Create a guest user to play games as a guest.",
)
async def guest_login(payload: GuestLoginRequest):
    """Create a guest user and return auth details."""
    if not payload.name or len(payload.name) > 32:
        raise HTTPException(
            status_code=400, detail="Name required and must be max 32 chars"
        )
    user = create_guest_user(payload.name)
    token = str(uuid4())  # For demo, no real JWT
    return LoginResponse(user=user, token=token)
