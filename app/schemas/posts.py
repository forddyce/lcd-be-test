from pydantic import BaseModel, Field
from datetime import datetime

class PostCreate(BaseModel):
    """
    create new post, validates text content of post
    """
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000, # adjust as needed
        example="This is my first post on the new platform!",
        description="The content of the user's post."
    )

class PostResponse(BaseModel):
    """
    return post detail, with unique id and timestamp
    """
    post_id: str = Field(..., example="abcd-1234-efgh-5678", description="Unique identifier for the post.")
    text: str = Field(..., description="The content of the post.")
    created_at: datetime = Field(..., description="Timestamp when the post was created.")

    class Config:
        """
        ORM mode. Allows the model to be created from arbitrary class instances that have the same field names
        as the model's fields, even if they are not dicts.
        """
        from_attributes = True