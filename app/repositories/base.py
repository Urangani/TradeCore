from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class Repository(Generic[ModelT]):
    def __init__(self, model_cls: type[ModelT], db: Session):
        self.model_cls = model_cls
        self.db = db

    def create(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get(self, item_id: int) -> ModelT | None:
        return self.db.get(self.model_cls, item_id)

    def list(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        stmt = select(self.model_cls).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())
