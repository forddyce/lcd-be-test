from fastapi import HTTPException, status

class UserAlreadyExistsException(HTTPException):
    """
    user email already exists, when register
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )

class InvalidCredentialsException(HTTPException):
    """
    wrong login email/password
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

class PostNotFoundException(HTTPException):
    """
    post not found
    """
    def __init__(self, post_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID '{post_id}' not found."
        )

class UnauthorizedAccessException(HTTPException):
    """
    when user tries to modify something that's not theirs
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized."
        )
