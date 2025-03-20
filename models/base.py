from datetime import timezone, datetime
import re

from sqlalchemy import func, BigInteger
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        cls_name = cls.__name__.lower()

        words = re.sub(
            "([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", cls_name)
        ).split()
        tablename = "_".join(words).lower() + "s"

        return tablename

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        server_default=func.now(),
        nullable=False,
    )
