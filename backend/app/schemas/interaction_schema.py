from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


InteractionType = Literal["Meeting", "Call", "Email", "Conference", "Follow-up", "Other"]
Sentiment = Literal["Positive", "Neutral", "Negative"]
Priority = Literal["Low", "Medium", "High"]
InteractionQuerySortBy = Literal[
    "created_at",
    "updated_at",
    "interaction_datetime",
    "hcp_name",
    "priority",
    "sentiment",
    "follow_up_date",
]
SortOrder = Literal["asc", "desc"]


class InteractionBase(BaseModel):
    hcp_name: str = Field(..., min_length=2, max_length=160)
    hcp_specialty: str | None = None
    organization: str | None = None
    interaction_type: InteractionType = "Meeting"
    interaction_datetime: datetime
    discussion_summary: str = Field(..., min_length=5)
    products_discussed: str | None = None
    samples_requested: str | None = None
    follow_up_required: bool = False
    follow_up_date: datetime | None = None
    representative_notes: str | None = None
    sentiment: Sentiment = "Neutral"
    priority: Priority = "Medium"
    ai_summary: str | None = None
    ai_insights: dict[str, Any] | None = None
    next_best_action: str | None = None


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    hcp_name: str | None = Field(default=None, min_length=2, max_length=160)
    hcp_specialty: str | None = None
    organization: str | None = None
    interaction_type: InteractionType | None = None
    interaction_datetime: datetime | None = None
    discussion_summary: str | None = Field(default=None, min_length=5)
    products_discussed: str | None = None
    samples_requested: str | None = None
    follow_up_required: bool | None = None
    follow_up_date: datetime | None = None
    representative_notes: str | None = None
    sentiment: Sentiment | None = None
    priority: Priority | None = None
    ai_summary: str | None = None
    ai_insights: dict[str, Any] | None = None
    next_best_action: str | None = None


class InteractionRead(InteractionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InteractionQueryResponse(BaseModel):
    total: int
    count: int
    limit: int
    offset: int
    items: list[InteractionRead]


class AgentChatRequest(BaseModel):
    message: str = Field(..., min_length=2)
    conversation: list[dict[str, str]] = Field(default_factory=list)


class ToolRequest(BaseModel):
    interaction_id: int | None = None
    message: str | None = None
    interaction_data: dict[str, Any] | None = None
    updates: dict[str, Any] | None = None
    raw_notes: str | None = None


class AgentResponse(BaseModel):
    intent: str
    status: str
    message: str
    data: dict[str, Any] | None = None
    missing_fields: list[str] = Field(default_factory=list)
