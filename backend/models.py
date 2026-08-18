import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


def _uuid():
    return str(uuid.uuid4())


def _now():
    return datetime.now(timezone.utc)


class Household(Base):
    __tablename__ = "households"

    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String, nullable=False)

    members = relationship("Member", back_populates="household")
    chores = relationship("Chore", back_populates="household")


class Member(Base):
    __tablename__ = "members"

    id = Column(String, primary_key=True, default=_uuid)
    household_id = Column(String, ForeignKey("households.id"), nullable=False)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)

    household = relationship("Household", back_populates="members")


class Chore(Base):
    __tablename__ = "chores"

    id = Column(String, primary_key=True, default=_uuid)
    household_id = Column(String, ForeignKey("households.id"), nullable=False)
    name = Column(String, nullable=False)
    weight = Column(Float, nullable=False, default=1.0)
    location = Column(String, nullable=True)

    household = relationship("Household", back_populates="chores")
    tags = relationship("Tag", back_populates="chore")


class Tag(Base):
    """物理NFCタグ1枚に対応する。tag.id がURL上のtagIdになる（推測困難なUUID）。"""

    __tablename__ = "tags"

    id = Column(String, primary_key=True, default=_uuid)
    chore_id = Column(String, ForeignKey("chores.id"), nullable=False)
    created_at = Column(DateTime, default=_now)

    chore = relationship("Chore", back_populates="tags")


class Record(Base):
    __tablename__ = "records"

    id = Column(String, primary_key=True, default=_uuid)
    chore_id = Column(String, ForeignKey("chores.id"), nullable=False)
    member_id = Column(String, ForeignKey("members.id"), nullable=False)
    recorded_at = Column(DateTime, default=_now)
    weight_snapshot = Column(Float, nullable=False)
    undone_at = Column(DateTime, nullable=True)

    chore = relationship("Chore")
    member = relationship("Member")
