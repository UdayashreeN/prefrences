from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, UniqueConstraint, ForeignKey
from .database import Base


class Preference(Base):
      __tablename__ = "preferences"
      id = Column(Integer, primary_key=True, index=True)
      user_id = Column(Integer, index=True, nullable=False)
      language = Column(String(16), nullable=False, default="en")
      theme = Column(String(32), nullable=False, default="light")
      notifications_enabled = Column(Boolean, nullable=False, default=True)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
      updated_at = Column(DateTime(timezone=True), onupdate=func.now())


      __table_args__ = (
            UniqueConstraint('user_id', name='uq_preferences_user_id'),
      )