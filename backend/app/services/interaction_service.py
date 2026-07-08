from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session

from app.models.interaction import Interaction
from app.schemas.interaction_schema import InteractionCreate, InteractionQuerySortBy, InteractionUpdate, SortOrder


class InteractionService:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Interaction]:
        return self.db.query(Interaction).order_by(desc(Interaction.created_at)).all()

    def query(
        self,
        *,
        q: str | None = None,
        hcp_name: str | None = None,
        organization: str | None = None,
        interaction_type: str | None = None,
        sentiment: str | None = None,
        priority: str | None = None,
        follow_up_required: bool | None = None,
        follow_up_due: bool | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
        sort_by: InteractionQuerySortBy = "created_at",
        sort_order: SortOrder = "desc",
    ) -> dict[str, Any]:
        query = self.db.query(Interaction)

        if q:
            pattern = f"%{q.strip()}%"
            query = query.filter(
                or_(
                    Interaction.hcp_name.ilike(pattern),
                    Interaction.hcp_specialty.ilike(pattern),
                    Interaction.organization.ilike(pattern),
                    Interaction.discussion_summary.ilike(pattern),
                    Interaction.products_discussed.ilike(pattern),
                    Interaction.samples_requested.ilike(pattern),
                    Interaction.representative_notes.ilike(pattern),
                    Interaction.ai_summary.ilike(pattern),
                    Interaction.next_best_action.ilike(pattern),
                )
            )
        if hcp_name:
            query = query.filter(Interaction.hcp_name.ilike(f"%{hcp_name.strip()}%"))
        if organization:
            query = query.filter(Interaction.organization.ilike(f"%{organization.strip()}%"))
        if interaction_type:
            query = query.filter(Interaction.interaction_type == interaction_type)
        if sentiment:
            query = query.filter(Interaction.sentiment == sentiment)
        if priority:
            query = query.filter(Interaction.priority == priority)
        if follow_up_required is not None:
            query = query.filter(Interaction.follow_up_required.is_(follow_up_required))
        if follow_up_due is True:
            query = query.filter(
                Interaction.follow_up_required.is_(True),
                Interaction.follow_up_date.is_not(None),
                Interaction.follow_up_date <= datetime.utcnow(),
            )
        if date_from:
            query = query.filter(Interaction.interaction_datetime >= date_from)
        if date_to:
            query = query.filter(Interaction.interaction_datetime <= date_to)

        total = query.with_entities(func.count(Interaction.id)).scalar() or 0
        sort_column = getattr(Interaction, sort_by)
        sort_expression = asc(sort_column) if sort_order == "asc" else desc(sort_column)
        items = query.order_by(sort_expression, desc(Interaction.id)).offset(offset).limit(limit).all()

        return {
            "total": total,
            "count": len(items),
            "limit": limit,
            "offset": offset,
            "items": items,
        }

    def get(self, interaction_id: int) -> Interaction:
        interaction = self.db.get(Interaction, interaction_id)
        if not interaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interaction {interaction_id} was not found.",
            )
        return interaction

    def create(self, payload: InteractionCreate | dict[str, Any]) -> Interaction:
        data = payload.model_dump() if isinstance(payload, InteractionCreate) else payload
        interaction = Interaction(**data)
        self.db.add(interaction)
        self.db.commit()
        self.db.refresh(interaction)
        return interaction

    def update(self, interaction_id: int, payload: InteractionUpdate | dict[str, Any]) -> Interaction:
        interaction = self.get(interaction_id)
        data = payload.model_dump(exclude_unset=True) if isinstance(payload, InteractionUpdate) else payload
        for key, value in data.items():
            if hasattr(interaction, key):
                setattr(interaction, key, value)
        interaction.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(interaction)
        return interaction

    def delete(self, interaction_id: int) -> None:
        interaction = self.get(interaction_id)
        self.db.delete(interaction)
        self.db.commit()
