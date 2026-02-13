from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import IntegrityError


def get_preferences_by_user(db: Session, user_id: int):
     return db.query(models.Preference).filter(models.Preference.user_id == user_id).first()


def create_preferences(db: Session, pref: schemas.PreferenceCreate):
     db_pref = models.Preference(
        user_id=pref.user_id,
        language=pref.language,
        theme=pref.theme,
        notifications_enabled=pref.notifications_enabled,
     )
     db.add(db_pref)
     try:
        db.commit()
        db.refresh(db_pref)
     except IntegrityError:
        db.rollback()
        raise
     return db_pref


def update_preferences(db: Session, user_id: int, updates: schemas.PreferenceUpdate):
    db_pref = get_preferences_by_user(db, user_id)
    if not db_pref:
        return None
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_pref, field, value)
    db.add(db_pref)
    db.commit()
    db.refresh(db_pref)
    return db_pref


# Upsert helper: create if missing, otherwise update
def upsert_preferences(db: Session, pref: schemas.PreferenceCreate):
    db_pref = get_preferences_by_user(db, pref.user_id)
    if db_pref:
       return update_preferences(db, pref.user_id, pref)
    return create_preferences(db, pref)