from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civiclegal.corpus_access import LegalRecord
from civiclegal.litigation_hold import flag_litigation_hold_candidates
from civiclegal.memo import draft_legal_memo


metadata = sa.MetaData()

legal_memo_records = sa.Table(
    "legal_memo_records",
    metadata,
    sa.Column("memo_id", sa.String(36), primary_key=True),
    sa.Column("topic", sa.String(255), nullable=False),
    sa.Column("sections", sa.JSON(), nullable=False),
    sa.Column("attorney_review_required", sa.Boolean(), nullable=False),
    sa.Column("not_legal_advice", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiclegal",
)

litigation_hold_records = sa.Table(
    "litigation_hold_records",
    metadata,
    sa.Column("hold_id", sa.String(36), primary_key=True),
    sa.Column("matter", sa.String(255), nullable=False),
    sa.Column("flagged_record_ids", sa.JSON(), nullable=False),
    sa.Column("hold_review_required", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiclegal",
)


@dataclass(frozen=True)
class StoredLegalMemo:
    memo_id: str
    topic: str
    sections: tuple[str, ...]
    attorney_review_required: bool
    not_legal_advice: bool
    created_at: datetime


@dataclass(frozen=True)
class StoredLitigationHold:
    hold_id: str
    matter: str
    flagged_record_ids: tuple[str, ...]
    hold_review_required: bool
    created_at: datetime


class LegalWorkpaperRepository:
    """SQLAlchemy-backed legal memo and litigation-hold workpaper records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civiclegal": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civiclegal"))
        metadata.create_all(self.engine)

    def create_memo(self, *, topic: str, cited_sources: list[str]) -> StoredLegalMemo:
        draft = draft_legal_memo(topic, cited_sources)
        stored = StoredLegalMemo(
            memo_id=str(uuid4()),
            topic=draft.topic,
            sections=draft.sections,
            attorney_review_required=draft.attorney_review_required,
            not_legal_advice=draft.not_legal_advice,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                legal_memo_records.insert().values(
                    memo_id=stored.memo_id,
                    topic=stored.topic,
                    sections=list(stored.sections),
                    attorney_review_required=stored.attorney_review_required,
                    not_legal_advice=stored.not_legal_advice,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_memo(self, memo_id: str) -> StoredLegalMemo | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(legal_memo_records).where(legal_memo_records.c.memo_id == memo_id)
            ).mappings().first()
        if row is None:
            return None
        data = dict(row)
        return StoredLegalMemo(
            memo_id=data["memo_id"],
            topic=data["topic"],
            sections=tuple(data["sections"]),
            attorney_review_required=data["attorney_review_required"],
            not_legal_advice=data["not_legal_advice"],
            created_at=data["created_at"],
        )

    def create_litigation_hold(
        self, *, matter: str, records: list[LegalRecord]
    ) -> StoredLitigationHold:
        flag = flag_litigation_hold_candidates(matter, records)
        stored = StoredLitigationHold(
            hold_id=str(uuid4()),
            matter=flag.matter,
            flagged_record_ids=flag.flagged_record_ids,
            hold_review_required=flag.hold_review_required,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                litigation_hold_records.insert().values(
                    hold_id=stored.hold_id,
                    matter=stored.matter,
                    flagged_record_ids=list(stored.flagged_record_ids),
                    hold_review_required=stored.hold_review_required,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_litigation_hold(self, hold_id: str) -> StoredLitigationHold | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(litigation_hold_records).where(
                    litigation_hold_records.c.hold_id == hold_id
                )
            ).mappings().first()
        if row is None:
            return None
        data = dict(row)
        return StoredLitigationHold(
            hold_id=data["hold_id"],
            matter=data["matter"],
            flagged_record_ids=tuple(data["flagged_record_ids"]),
            hold_review_required=data["hold_review_required"],
            created_at=data["created_at"],
        )
