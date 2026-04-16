from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, Brochure

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class BrochureOut(BaseModel):
    id: int
    company_name: str
    url: str
    markdown: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/brochures", response_model=list[BrochureOut])
def get_brochures(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Brochure).filter(Brochure.owner_id == user.id).order_by(Brochure.created_at.desc()).all()


@router.delete("/brochures/{brochure_id}")
def delete_brochure(brochure_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    b = db.query(Brochure).filter(Brochure.id == brochure_id, Brochure.owner_id == user.id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Brochure not found")
    db.delete(b)
    db.commit()
    return {"detail": "Deleted"}
