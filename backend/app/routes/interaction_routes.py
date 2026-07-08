from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.interaction_schema import (
    InteractionCreate,
    InteractionQueryResponse,
    InteractionQuerySortBy,
    InteractionRead,
    InteractionType,
    InteractionUpdate,
    Priority,
    Sentiment,
    SortOrder,
)
from app.services.interaction_service import InteractionService


router = APIRouter(prefix="/api/interactions", tags=["interactions"])


@router.post("", response_model=InteractionRead, status_code=status.HTTP_201_CREATED)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    return InteractionService(db).create(payload)


@router.get("", response_model=list[InteractionRead])
def list_interactions(db: Session = Depends(get_db)):
    return InteractionService(db).list()


@router.get("/query", response_model=InteractionQueryResponse)
def query_interactions(
    q: str | None = Query(default=None, min_length=1, max_length=200),
    hcp_name: str | None = Query(default=None, min_length=1, max_length=160),
    organization: str | None = Query(default=None, min_length=1, max_length=220),
    interaction_type: InteractionType | None = None,
    sentiment: Sentiment | None = None,
    priority: Priority | None = None,
    follow_up_required: bool | None = None,
    follow_up_due: bool | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: InteractionQuerySortBy = "created_at",
    sort_order: SortOrder = "desc",
    db: Session = Depends(get_db),
):
    return InteractionService(db).query(
        q=q,
        hcp_name=hcp_name,
        organization=organization,
        interaction_type=interaction_type,
        sentiment=sentiment,
        priority=priority,
        follow_up_required=follow_up_required,
        follow_up_due=follow_up_due,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/{interaction_id}", response_model=InteractionRead)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    return InteractionService(db).get(interaction_id)


@router.put("/{interaction_id}", response_model=InteractionRead)
def update_interaction(interaction_id: int, payload: InteractionUpdate, db: Session = Depends(get_db)):
    return InteractionService(db).update(interaction_id, payload)


@router.delete("/{interaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    InteractionService(db).delete(interaction_id)
    return None
