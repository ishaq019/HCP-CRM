from datetime import datetime
import json
from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agents.prompts import (
    EDIT_EXTRACTION_PROMPT,
    EXTRACT_INTERACTION_PROMPT,
    FOLLOWUP_PROMPT,
    INSIGHTS_PROMPT,
    SUMMARY_PROMPT,
)
from app.schemas.interaction_schema import InteractionCreate, InteractionRead, InteractionUpdate
from app.services.interaction_service import InteractionService
from app.services.llm_service import LLMService


REQUIRED_FIELDS = ["hcp_name", "interaction_type", "interaction_datetime", "discussion_summary"]


class LogInteractionInput(BaseModel):
    interaction_data: dict[str, Any] | None = Field(default=None)
    raw_text: str | None = Field(default=None)


class EditInteractionInput(BaseModel):
    interaction_id: int
    updates: dict[str, Any] | None = Field(default=None)
    edit_request: str | None = Field(default=None)


class SummarizeInteractionInput(BaseModel):
    interaction_id: int | None = None
    raw_notes: str | None = None


class SuggestFollowupInput(BaseModel):
    interaction_id: int | None = None
    interaction_data: dict[str, Any] | None = None


class ExtractInsightsInput(BaseModel):
    interaction_id: int | None = None
    interaction_data: dict[str, Any] | None = None
    raw_notes: str | None = None


def serialize_interaction(interaction: Any) -> dict[str, Any]:
    return InteractionRead.model_validate(interaction).model_dump(mode="json")


def content_from_interaction(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, default=str)


def missing_required_fields(data: dict[str, Any]) -> list[str]:
    return [field for field in REQUIRED_FIELDS if not data.get(field)]


def clean_create_payload(data: dict[str, Any]) -> dict[str, Any]:
    allowed = set(InteractionCreate.model_fields.keys())
    return {key: value for key, value in data.items() if key in allowed and value is not None}


def clean_update_payload(data: dict[str, Any]) -> dict[str, Any]:
    allowed = set(InteractionUpdate.model_fields.keys())
    return {key: value for key, value in data.items() if key in allowed}


def create_tool_registry(db: Session, llm: LLMService) -> dict[str, StructuredTool]:
    service = InteractionService(db)

    def log_interaction(interaction_data: dict[str, Any] | None = None, raw_text: str | None = None) -> dict[str, Any]:
        data = dict(interaction_data or {})
        if raw_text:
            extracted = llm.invoke_json(
                EXTRACT_INTERACTION_PROMPT,
                {"message": raw_text, "current_datetime": datetime.utcnow().isoformat()},
            )
            data = {**extracted, **data}

        missing = missing_required_fields(data)
        if missing:
            return {
                "status": "validation_error",
                "message": "Required fields are missing.",
                "missing_fields": missing,
                "draft": data,
            }

        summary_source = data.get("representative_notes") or data.get("discussion_summary") or content_from_interaction(data)
        ai_summary = llm.invoke_text(SUMMARY_PROMPT, {"content": summary_source})
        insights = llm.invoke_json(INSIGHTS_PROMPT, {"content": content_from_interaction(data)})
        followup = llm.invoke_json(
            FOLLOWUP_PROMPT,
            {"content": content_from_interaction(data), "current_datetime": datetime.utcnow().isoformat()},
        )

        data["ai_summary"] = ai_summary
        data["ai_insights"] = insights
        data["next_best_action"] = followup.get("next_best_action")
        payload = InteractionCreate.model_validate(clean_create_payload(data))
        interaction = service.create(payload)
        return {
            "status": "success",
            "message": "Interaction logged successfully.",
            "interaction": serialize_interaction(interaction),
            "followup_recommendation": followup,
        }

    def edit_interaction(
        interaction_id: int,
        updates: dict[str, Any] | None = None,
        edit_request: str | None = None,
    ) -> dict[str, Any]:
        current = serialize_interaction(service.get(interaction_id))
        next_updates = dict(updates or {})
        if edit_request:
            extracted_updates = llm.invoke_json(
                EDIT_EXTRACTION_PROMPT,
                {"current_record": content_from_interaction(current), "edit_request": edit_request},
            )
            next_updates.update(extracted_updates)
        if not next_updates:
            return {"status": "validation_error", "message": "No updates were provided.", "interaction": current}
        validated_updates = InteractionUpdate.model_validate(clean_update_payload(next_updates)).model_dump(
            exclude_unset=True
        )
        updated = service.update(interaction_id, validated_updates)
        return {
            "status": "success",
            "message": "Interaction updated successfully.",
            "interaction": serialize_interaction(updated),
        }

    def summarize_interaction(interaction_id: int | None = None, raw_notes: str | None = None) -> dict[str, Any]:
        if interaction_id:
            content = content_from_interaction(serialize_interaction(service.get(interaction_id)))
        elif raw_notes:
            content = raw_notes
        else:
            return {"status": "validation_error", "message": "Provide interaction_id or raw_notes."}
        summary = llm.invoke_text(SUMMARY_PROMPT, {"content": content})
        if interaction_id:
            service.update(interaction_id, {"ai_summary": summary})
        return {"status": "success", "message": "Summary generated.", "summary": summary}

    def suggest_followup(
        interaction_id: int | None = None,
        interaction_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if interaction_id:
            data = serialize_interaction(service.get(interaction_id))
        elif interaction_data:
            data = interaction_data
        else:
            return {"status": "validation_error", "message": "Provide interaction_id or interaction_data."}
        recommendation = llm.invoke_json(
            FOLLOWUP_PROMPT,
            {"content": content_from_interaction(data), "current_datetime": datetime.utcnow().isoformat()},
        )
        if interaction_id and recommendation.get("next_best_action"):
            service.update(interaction_id, {"next_best_action": recommendation["next_best_action"]})
        return {"status": "success", "message": "Follow-up recommendation generated.", "recommendation": recommendation}

    def extract_hcp_insights(
        interaction_id: int | None = None,
        interaction_data: dict[str, Any] | None = None,
        raw_notes: str | None = None,
    ) -> dict[str, Any]:
        if interaction_id:
            data = serialize_interaction(service.get(interaction_id))
            content = content_from_interaction(data)
        elif interaction_data:
            content = content_from_interaction(interaction_data)
        elif raw_notes:
            content = raw_notes
        else:
            return {"status": "validation_error", "message": "Provide interaction_id, interaction_data, or raw_notes."}
        insights = llm.invoke_json(INSIGHTS_PROMPT, {"content": content})
        if interaction_id:
            service.update(interaction_id, {"ai_insights": insights})
        return {"status": "success", "message": "HCP insights extracted.", "insights": insights}

    return {
        "log_interaction": StructuredTool.from_function(
            func=log_interaction,
            name="log_interaction",
            description="Capture, validate, enrich with LLM summary/insights/follow-up, and save an HCP interaction.",
            args_schema=LogInteractionInput,
        ),
        "edit_interaction": StructuredTool.from_function(
            func=edit_interaction,
            name="edit_interaction",
            description="Modify an existing interaction using structured fields or a conversational edit request.",
            args_schema=EditInteractionInput,
        ),
        "summarize_interaction": StructuredTool.from_function(
            func=summarize_interaction,
            name="summarize_interaction",
            description="Generate a short professional summary from raw notes or a saved interaction.",
            args_schema=SummarizeInteractionInput,
        ),
        "suggest_followup": StructuredTool.from_function(
            func=suggest_followup,
            name="suggest_followup",
            description="Recommend the next best action and urgency for a representative.",
            args_schema=SuggestFollowupInput,
        ),
        "extract_insights": StructuredTool.from_function(
            func=extract_hcp_insights,
            name="extract_insights",
            description="Extract HCP interest level, objections, product interest, and opportunity.",
            args_schema=ExtractInsightsInput,
        ),
    }
