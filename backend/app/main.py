from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.brochure import router as brochure_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models.user import User, Brochure  # noqa: F401 — registers tables

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(brochure_router)
app.include_router(dashboard_router)
