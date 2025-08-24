from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, auth

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
