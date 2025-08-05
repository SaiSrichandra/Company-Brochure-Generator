from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.brochure import router as brochure_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brochure_router)
