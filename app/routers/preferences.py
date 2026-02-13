from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from typing import Any


from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/preferences", tags=["preferences"])

@router.post("/", response_model=schemas.PreferenceOut, status_code=status.HTTP_201_CREATED)
def create_or_replace_preferences(pref_in: schemas.PreferenceCreate, db: Session = Depends(get_db)):
      existing = crud.get_preferences_by_user(db, pref_in.user_id)
      if existing:
          # replace: update all fields
          updated = crud.update_preferences(db, pref_in.user_id, pref_in)
          if not updated:
              raise HTTPException(status_code=500, detail="Failed to update preferences")
          return updated
      return crud.create_preferences(db, pref_in)



@router.get("/{user_id}", response_model=schemas.PreferenceOut)
def read_preferences(user_id: int, db: Session = Depends(get_db)):
     db_pref = crud.get_preferences_by_user(db, user_id)
     if not db_pref:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")
     return db_pref


@router.patch("/{user_id}", response_model=schemas.PreferenceOut)
def patch_preferences(user_id: int, updates: schemas.PreferenceUpdate, db: Session = Depends(get_db)):
      updated = crud.update_preferences(db, user_id, updates)
      if not updated:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found")
      return updated