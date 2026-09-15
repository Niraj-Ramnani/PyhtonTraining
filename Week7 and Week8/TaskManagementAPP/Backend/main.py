from fastapi import FastAPI
from src.utils.db import Base , engine
from src.tasks.route import task_routes
from src.user.route import user_routes
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(engine)
app = FastAPI(title="Task Management App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(task_routes, tags=["tasks"])
app.include_router(user_routes , tags=["users"])

