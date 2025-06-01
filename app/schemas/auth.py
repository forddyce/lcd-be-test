from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """
    user registration, check email is valid and password length is OK
    """
    email: EmailStr = Field(..., example="user@example.com", description="User's email address.")
    password: str = Field(..., min_length=8, max_length=64, description="User's password (min 8, max 64 characters).")

class UserLogin(BaseModel):
    """
    user login, check for email and password when authenticate user
    """
    email: EmailStr = Field(..., example="user@example.com", description="User's email address.")
    password: str = Field(..., description="User's password.")

class Token(BaseModel):
    """
    user auth token response, making sure it has access token and has a type (ex. bearer)
    """
    access_token: str = Field(..., description="The JWT or randomly generated authentication token.")
    token_type: str = Field("bearer", description="Type of the token, typically 'bearer'.")

class TokenData(BaseModel):
    """
    used for dependency injection to get the current user's email.
    """
    email: str | None = Field(default=None, description="Email extracted from the token payload.")