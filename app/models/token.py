from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone

from app.db.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    token = Column(String, unique=True, nullable=False, index=True)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )