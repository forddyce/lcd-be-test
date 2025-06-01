from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.posts import PostCreate, PostResponse
from app.services.post_service import PostService
from app.core.dependencies import get_current_user
from app.database.models import User # To type-hint the current_user
from app.core.exceptions import PostNotFoundException
from app.core.config import settings

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/add", response_model=str, status_code=status.HTTP_201_CREATED)
async def add_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(PostService),
    request: Request = Request
):
    """
    create user for current authenticated user,
    validates payload size and stores the post in memory
    """
    # content_length = request.headers.get("Content-Length")
    # if content_length and int(content_length) > settings.MAX_PAYLOAD_SIZE_BYTES:
    #     raise HTTPException(
    #         status_code=status.HTTP_413_PAYLOAD_TOO_LARGE,
    #         detail=f"Payload size exceeds the maximum limit of {settings.MAX_PAYLOAD_SIZE_MB}MB."
    #     )
    try:
        post_id = post_service.add_post(current_user.email, post_data)
        return post_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while adding the post: {e}"
        )


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(PostService)
):
    """
    gets all posts belonging to current user,
    implements memory response caching for up to 5 minutes per user
    """
    try:
        posts = post_service.get_user_posts(current_user.email)
        return posts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while retrieving posts: {e}"
        )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(PostService)
):
    """
    deletes a post belonging to current user
    """
    try:
        post_service.delete_post(current_user.email, post_id)
        # 204
    except PostNotFoundException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the post: {e}"
        )
