from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import users, calculations
import os
from pathlib import Path

# Create database tables only if not in test mode
if os.getenv("TESTING") != "true":
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Calculator",
    description="A calculator API with user authentication and calculation history",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

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
