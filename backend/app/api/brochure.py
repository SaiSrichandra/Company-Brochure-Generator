from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from app.services.brochure_service import generate_brochure_text
import os

router = APIRouter()

class BrochureRequest(BaseModel):
    company_name: str
    url: HttpUrl

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://company-brochure-generator.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post("/generate-brochure")
def generate_brochure(req: BrochureRequest):
    try:
        brochure_md = generate_brochure_text(str(req.company_name), str(req.url))
        return {"markdown": brochure_md}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
