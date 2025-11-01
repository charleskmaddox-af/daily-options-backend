from datetime import date, datetime

from sqlalchemy import (
    String, Integer, Numeric, Boolean, Date, TIMESTAMP, func
)
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class DailyChecklist(Base):
    __tablename__ = "daily_checklist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Use Python type in Mapped[...] and SQL type in mapped_column(...)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)

    open_csp_count: Mapped[int | None] = mapped_column(Integer)
    positions_rolled_count: Mapped[int | None] = mapped_column(Integer)
    cash_deployed_pct: Mapped[float | None] = mapped_column(Numeric(5, 2))
    high_impact_event: Mapped[bool | None] = mapped_column(Boolean)
    qqq_rsi_over70: Mapped[bool | None] = mapped_column(Boolean)
    notes: Mapped[str | None] = mapped_column(String(2000))

    # Must specify the concrete type for Mapped[...]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )


class OptionPositionSnapshot(Base):
    __tablename__ = "option_position_snapshot"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    option_symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    side: Mapped[str] = mapped_column(String(16), nullable=False)  # e.g., 'short_put'
    qty: Mapped[int] = mapped_column(Integer, nullable=False)

    avg_credit: Mapped[float | None] = mapped_column(Numeric(12, 4))
    mark_price: Mapped[float | None] = mapped_column(Numeric(12, 4))
    premium_returned_pct: Mapped[float | None] = mapped_column(Numeric(6, 2))
    dte: Mapped[int | None] = mapped_column(Integer)
    itm: Mapped[bool | None] = mapped_column(Boolean)
    underlying_price: Mapped[float | None] = mapped_column(Numeric(12, 4))
    iv: Mapped[float | None] = mapped_column(Numeric(8, 4))
    delta: Mapped[float | None] = mapped_column(Numeric(8, 4))
    gamma: Mapped[float | None] = mapped_column(Numeric(8, 4))
    theta: Mapped[float | None] = mapped_column(Numeric(8, 4))
    vega: Mapped[float | None] = mapped_column(Numeric(8, 4))

    asof: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

