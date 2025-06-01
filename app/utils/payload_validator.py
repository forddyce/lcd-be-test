from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings

class MaxPayloadSizeMiddleware(BaseHTTPMiddleware):
    """
    fastapi middleware to restrict the maximum payload size for incoming requests.
    """
    def __init__(self, app):
        super().__init__(app)
        self.max_size_bytes = settings.MAX_PAYLOAD_SIZE_BYTES

    async def dispatch(self, request: Request, call_next):
        """
        Dispatches the request through the middleware.
        """
        # only apply this check to POST requests, specifically for the AddPost endpoint, or somehting similar
        # we can make this more specific if needed, like, check request.url.path
        if request.method == "POST":
            content_length = request.headers.get("Content-Length")
            if content_length:
                try:
                    if int(content_length) > self.max_size_bytes:
                        return JSONResponse(
                            status_code=status.HTTP_413_PAYLOAD_TOO_LARGE,
                            content={"detail": f"Payload size exceeds the maximum limit of {settings.MAX_PAYLOAD_SIZE_MB}MB."}
                        )
                except ValueError:
                    # Content-Length is not a valid integer
                    pass
        return await call_next(request)