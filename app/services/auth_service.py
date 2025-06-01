from sqlalchemy.orm import Session
from app.database.models import User
from app.schemas.auth import UserCreate, UserLogin, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsException, InvalidCredentialsException

class AuthService:
    def signup_user(self, db: Session, user_data: UserCreate) -> Token:
        """
        register new user
        """
        db_user = db.query(User).filter(User.email == user_data.email).first()
        if db_user:
            raise UserAlreadyExistsException()

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user) # refresh to get the auto-generated ID and timestamps

        access_token = create_access_token(data={"sub": new_user.email})
        return Token(access_token=access_token, token_type="bearer")

    def login_user(self, db: Session, user_data: UserLogin) -> Token:
        """
        user login, return token after success
        """
        user = db.query(User).filter(User.email == user_data.email).first()

        if not user or not verify_password(user_data.password, user.hashed_password):
            raise InvalidCredentialsException()

        access_token = create_access_token(data={"sub": user.email})

        return Token(access_token=access_token, token_type="bearer")