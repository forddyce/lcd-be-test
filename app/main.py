from fastapi import FastAPI
from app.api.v1.endpoints import auth, posts
from app.database.session import init_db
from app.utils.payload_validator import MaxPayloadSizeMiddleware

app = FastAPI(
    title="Lucid BE Test",
    description="A simple FastAPI app, but the posts are user in-memory caching.",
    version="0.0.1"
)

@app.on_event("startup")
async def startup_event():
    init_db()

app.add_middleware(MaxPayloadSizeMiddleware)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Welcome to the FastAPI MVC Post Application! Visit /docs for API documentation."}
