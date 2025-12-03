from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, calculations
import os

# Create database tables only if not in test mode
if os.getenv("TESTING") != "true":
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Calculator",
    description="A calculator API with user authentication and calculation history",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(calculations.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to FastAPI Calculator API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
