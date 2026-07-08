from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.hcp_agent import HCPAgent
from app.database import get_db
from app.schemas.interaction_schema import AgentChatRequest, AgentResponse, ToolRequest
from app.services.llm_service import MissingGroqApiKeyError, raise_ai_configuration_error


router = APIRouter(prefix="/api/agent", tags=["agent"])


def run_agent(db: Session, state: dict) -> dict:
    try:
        return HCPAgent(db).invoke(state)
    except MissingGroqApiKeyError as exc:
        raise_ai_configuration_error(exc)


@router.post("/chat", response_model=AgentResponse)
def chat(payload: AgentChatRequest, db: Session = Depends(get_db)):
    return run_agent(
        db,
        {
            "route": "chat",
            "message": payload.message,
            "conversation": payload.conversation,
        },
    )


@router.post("/log-interaction", response_model=AgentResponse)
def log_interaction(payload: ToolRequest, db: Session = Depends(get_db)):
    return run_agent(
        db,
        {
            "route": "tool",
            "intent": "log_interaction",
            "payload": {"interaction_data": payload.interaction_data, "raw_text": payload.message},
        },
    )


@router.post("/edit-interaction", response_model=AgentResponse)
def edit_interaction(payload: ToolRequest, db: Session = Depends(get_db)):
    return run_agent(
        db,
        {
            "route": "tool",
            "intent": "edit_interaction",
            "payload": {
                "interaction_id": payload.interaction_id,
                "updates": payload.updates,
                "edit_request": payload.message,
            },
        },
    )


@router.post("/summarize", response_model=AgentResponse)
def summarize(payload: ToolRequest, db: Session = Depends(get_db)):
    return run_agent(
        db,
        {
            "route": "tool",
            "intent": "summarize_interaction",
            "payload": {"interaction_id": payload.interaction_id, "raw_notes": payload.raw_notes or payload.message},
        },
    )


@router.post("/suggest-followup", response_model=AgentResponse)
def suggest_followup(payload: ToolRequest, db: Session = Depends(get_db)):
    return run_agent(
        db,
        {
            "route": "tool",
            "intent": "suggest_followup",
            "payload": {"interaction_id": payload.interaction_id, "interaction_data": payload.interaction_data},
        },
    )


@router.post("/extract-insights", response_model=AgentResponse)
def extract_insights(payload: ToolRequest, db: Session = Depends(get_db)):
    return run_agent(
        db,
        {
            "route": "tool",
            "intent": "extract_insights",
            "payload": {
                "interaction_id": payload.interaction_id,
                "interaction_data": payload.interaction_data,
                "raw_notes": payload.raw_notes or payload.message,
            },
        },
    )
