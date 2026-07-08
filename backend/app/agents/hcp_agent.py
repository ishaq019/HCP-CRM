from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.agents.graph import AgentState, build_hcp_graph
from app.agents.prompts import CLASSIFY_INTENT_PROMPT, EXTRACT_INTERACTION_PROMPT
from app.agents.tools import create_tool_registry, missing_required_fields
from app.services.llm_service import LLMService


class HCPAgent:
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMService()
        self.tools = create_tool_registry(db, self.llm)
        self.graph = build_hcp_graph(
            {
                "receive_user_input": self.receive_user_input,
                "classify_intent": self.classify_intent,
                "extract_interaction_data": self.extract_interaction_data,
                "validate_data": self.validate_data,
                "call_required_tool": self.call_required_tool,
                "generate_response": self.generate_response,
                "route_after_classification": self.route_after_classification,
                "route_after_validation": self.route_after_validation,
            }
        )

    def invoke(self, state: AgentState) -> dict[str, Any]:
        return self.graph.invoke(state).get("response", {})

    def receive_user_input(self, state: AgentState) -> AgentState:
        conversation_text = "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')}" for item in state.get("conversation", [])
        )
        message = state.get("message") or ""
        return {**state, "message": f"{conversation_text}\nuser: {message}".strip()}

    def classify_intent(self, state: AgentState) -> AgentState:
        if state.get("intent"):
            return state
        result = self.llm.invoke_json(CLASSIFY_INTENT_PROMPT, {"message": state.get("message", "")})
        return {**state, "intent": result.get("intent", "unknown")}

    def route_after_classification(self, state: AgentState) -> str:
        intent = state.get("intent")
        if intent == "log_interaction" and state.get("route") == "chat":
            return "extract"
        if intent in self.tools:
            return "tool"
        return "respond"

    def extract_interaction_data(self, state: AgentState) -> AgentState:
        draft = self.llm.invoke_json(
            EXTRACT_INTERACTION_PROMPT,
            {"message": state.get("message", ""), "current_datetime": datetime.utcnow().isoformat()},
        )
        return {**state, "draft": draft}

    def validate_data(self, state: AgentState) -> AgentState:
        missing = missing_required_fields(state.get("draft", {}))
        return {**state, "missing_fields": missing}

    def route_after_validation(self, state: AgentState) -> str:
        if state.get("route") == "chat":
            return "draft"
        return "tool"

    def call_required_tool(self, state: AgentState) -> AgentState:
        intent = state.get("intent", "")
        payload = dict(state.get("payload") or {})
        if state.get("draft"):
            payload.setdefault("interaction_data", state["draft"])
        tool = self.tools.get(intent)
        if not tool:
            return {**state, "tool_result": {"status": "error", "message": "No matching LangGraph tool was found."}}
        result = tool.invoke(payload)
        return {**state, "tool_result": result}

    def generate_response(self, state: AgentState) -> AgentState:
        if state.get("route") == "chat" and state.get("intent") == "log_interaction":
            missing = state.get("missing_fields", [])
            status = "needs_review" if missing else "draft_ready"
            response = {
                "intent": "log_interaction",
                "status": status,
                "message": "Review the extracted draft before saving.",
                "data": {"draft": state.get("draft", {})},
                "missing_fields": missing,
            }
            return {**state, "response": response}

        tool_result = state.get("tool_result")
        if tool_result:
            status = tool_result.get("status", "success")
            response = {
                "intent": state.get("intent", "unknown"),
                "status": status,
                "message": tool_result.get("message", "Tool completed."),
                "data": tool_result,
                "missing_fields": tool_result.get("missing_fields", []),
            }
            return {**state, "response": response}

        response = {
            "intent": state.get("intent", "unknown"),
            "status": "unknown_intent",
            "message": "I could not determine which CRM action to take. Try asking to log, edit, summarize, suggest follow-up, or extract insights.",
            "data": None,
            "missing_fields": [],
        }
        return {**state, "response": response}
