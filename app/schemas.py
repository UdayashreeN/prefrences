from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PreferenceBase(BaseModel):
       language: Optional[str] = Field(default="en", max_length=16)
       theme: Optional[str] = Field(default="light", max_length=32)
       notifications_enabled: Optional[bool] = True


class PreferenceCreate(PreferenceBase):
      user_id: int


class PreferenceUpdate(PreferenceBase):
      pass


class PreferenceOut(PreferenceBase):
      id: int
      user_id: int
      created_at: Optional[datetime]
      updated_at: Optional[datetime]


      class Config:
          orm_mode = True