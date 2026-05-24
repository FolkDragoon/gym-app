from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, Date
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    pass

class Member(Base):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    qr_code: Mapped[str] = mapped_column(String, unique=True)
    birthday: Mapped[datetime] = mapped_column(Date, nullable=False)
    subscription_months: Mapped[int] = mapped_column(Integer)
    subscription_expires: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    member_id: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)