from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AssetType(str, Enum):
    GRAM_18K = "18k_gram"
    HALF_COIN = "half_coin"
    QUARTER_COIN = "quarter_coin"
    BAHAR_COIN = "bahar_coin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    gram_18k: Mapped[float] = mapped_column(Float, default=0)
    half_coin: Mapped[float] = mapped_column(Float, default=0)
    quarter_coin: Mapped[float] = mapped_column(Float, default=0)
    bahar_coin: Mapped[float] = mapped_column(Float, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Holding(Base):
    __tablename__ = "holdings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_type: Mapped[str] = mapped_column(String(32), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
