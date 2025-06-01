from typing import List
from uuid import uuid4
from datetime import datetime, timedelta

from app.schemas.posts import PostCreate, PostResponse
from app.core.exceptions import PostNotFoundException
from app.core.config import settings
from app.utils.cache import InMemoryCache

# in-memory storage for posts.
# format: {user_email: {post_id: PostResponse}}
in_memory_posts = {}

posts_cache = InMemoryCache(ttl_minutes=settings.CACHE_TTL_MINUTES)

class PostService:
    """
    posts are stored memory, and retrieval of posts is cached.
    """
    def add_post(self, user_email: str, post_data: PostCreate) -> str:
        """
        adds a new post to memory storage for a specific user.
        """
        post_id = str(uuid4())
        current_time = datetime.now()

        new_post = PostResponse(
            post_id=post_id,
            text=post_data.text,
            created_at=current_time
        )

        # ensure the user's entry exists in our memory storage
        if user_email not in in_memory_posts:
            in_memory_posts[user_email] = {}

        in_memory_posts[user_email][post_id] = new_post

        # invalidate cache for this user's posts as new post is added
        posts_cache.invalidate(user_email)

        return post_id

    def get_user_posts(self, user_email: str) -> List[PostResponse]:
        """
        get all posts for a specific user from memory storage.
        """
        # check if post exists in cache
        cached_posts = posts_cache.get(user_email)
        if cached_posts:
            print(f"Retrieving posts for {user_email} from cache.")
            return cached_posts

        # if not in cache, retrieve from memory storage
        user_posts_dict = in_memory_posts.get(user_email, {})
        # Convert dict values to a list of PostResponse objects
        posts = sorted(list(user_posts_dict.values()), key=lambda p: p.created_at, reverse=True)

        # store posts in cache again
        posts_cache.set(user_email, posts)
        print(f"Retrieving posts for {user_email} from memory and added the posts to cache.")

        return posts

    def delete_post(self, user_email: str, post_id: str):
        """
        removes a specific post for a user from in-memory storage.
        """
        if user_email not in in_memory_posts:
            raise PostNotFoundException(post_id) # user has no posts at all

        if post_id not in in_memory_posts[user_email]:
            raise PostNotFoundException(post_id) # post not found for this user

        del in_memory_posts[user_email][post_id]
        posts_cache.invalidate(user_email)
        