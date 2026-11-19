from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CustomerRow(Base):
    __tablename__ = "api_customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)