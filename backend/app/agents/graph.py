from typing import Any, Literal, TypedDict

from langgraph.graph import END, StateGraph


class AgentState(TypedDict, total=False):
    message: str
    conversation: list[dict[str, str]]
    intent: str
    route: str
    payload: dict[str, Any]
    draft: dict[str, Any]
    missing_fields: list[str]
    tool_result: dict[str, Any]
    response: dict[str, Any]
    error: str


def build_hcp_graph(nodes: dict[str, Any]):
    graph = StateGraph(AgentState)
    graph.add_node("receive_user_input", nodes["receive_user_input"])
    graph.add_node("classify_intent", nodes["classify_intent"])
    graph.add_node("extract_interaction_data", nodes["extract_interaction_data"])
    graph.add_node("validate_data", nodes["validate_data"])
    graph.add_node("call_required_tool", nodes["call_required_tool"])
    graph.add_node("generate_response", nodes["generate_response"])

    graph.set_entry_point("receive_user_input")
    graph.add_edge("receive_user_input", "classify_intent")
    graph.add_conditional_edges(
        "classify_intent",
        nodes["route_after_classification"],
        {
            "extract": "extract_interaction_data",
            "tool": "call_required_tool",
            "respond": "generate_response",
        },
    )
    graph.add_edge("extract_interaction_data", "validate_data")
    graph.add_conditional_edges(
        "validate_data",
        nodes["route_after_validation"],
        {
            "draft": "generate_response",
            "tool": "call_required_tool",
        },
    )
    graph.add_edge("call_required_tool", "generate_response")
    graph.add_edge("generate_response", END)
    return graph.compile()
