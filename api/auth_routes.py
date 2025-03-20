from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.security import hash_password, verify_password
from core.jwt_handler import create_access_token, decode_access_token
from core.database import get_db
from models.models import User


router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """Validate JWT token and return the username."""
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["sub"]


@router.post('/register/')
async def register_user(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    """Register new user."""
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if user:
        raise HTTPException(status_code=400, detail='User already exists')

    new_user = User(username=username, password_hash=hash_password(password))
    db.add(new_user)
    await db.commit()

    return {'message': 'User successfully registered'}


@router.post('/login')
async def login_user(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    access_token = create_access_token({'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}
