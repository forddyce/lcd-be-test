from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth_service import AuthService
from app.core.dependencies import get_db
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(AuthService)
):
    """
    register user with email and password,
    returns access token on sucecss
    """
    try:
        token = auth_service.signup_user(db, user_data)
        return token
    except UserAlreadyExistsException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during signup: {e}"
        )

@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(AuthService)
):
    """
    authenticates the user,
    returns access token upon login
    """
    try:
        token = auth_service.login_user(db, user_data)
        return token
    except InvalidCredentialsException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during login: {e}"
        )