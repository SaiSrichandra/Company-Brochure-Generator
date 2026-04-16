from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from app.services.brochure_service import generate_brochure_text
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, Brochure

router = APIRouter()

class BrochureRequest(BaseModel):
    company_name: str
    url: str

@router.post("/generate-brochure")
def generate_brochure(req: BrochureRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        brochure_md = generate_brochure_text(str(req.company_name), str(req.url))
        brochure = Brochure(
            company_name=req.company_name,
            url=req.url,
            markdown=brochure_md,
            owner_id=user.id
        )
        db.add(brochure)
        db.commit()
        return {"markdown": brochure_md}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
