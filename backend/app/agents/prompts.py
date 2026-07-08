CLASSIFY_INTENT_PROMPT = """
You are the intent router for an AI-first CRM used by life sciences field representatives.
Classify the user message into exactly one intent:
log_interaction, edit_interaction, summarize_interaction, suggest_followup, extract_insights, unknown.

Return only JSON with this schema:
{{
  "intent": "log_interaction",
  "confidence": 0.0,
  "reason": "short reason"
}}

User message:
{message}
"""

EXTRACT_INTERACTION_PROMPT = """
You extract HCP interaction data for a CRM. Use the current date as context: {current_datetime}.
Read the conversation and return only JSON. If a field is unknown, use null. Dates must be ISO 8601.

Allowed interaction_type values: Meeting, Call, Email, Conference, Follow-up, Other.
Allowed sentiment values: Positive, Neutral, Negative.
Allowed priority values: Low, Medium, High.

JSON schema:
{{
  "hcp_name": null,
  "hcp_specialty": null,
  "organization": null,
  "interaction_type": "Meeting",
  "interaction_datetime": null,
  "discussion_summary": null,
  "products_discussed": null,
  "samples_requested": null,
  "follow_up_required": false,
  "follow_up_date": null,
  "representative_notes": null,
  "sentiment": "Neutral",
  "priority": "Medium"
}}

Conversation:
{message}
"""

SUMMARY_PROMPT = """
Create a concise, professional CRM summary for this HCP interaction.
Keep it to 2-3 sentences and avoid unsupported claims.

Interaction or notes:
{content}
"""

FOLLOWUP_PROMPT = """
You recommend next best actions for life sciences field representatives.
Analyze the interaction and return only JSON.

JSON schema:
{{
  "next_best_action": "specific action",
  "urgency": "Low|Medium|High",
  "suggested_follow_up_date": null,
  "rationale": "short rationale"
}}

Current date/time: {current_datetime}
Interaction:
{content}
"""

INSIGHTS_PROMPT = """
Extract sales insights from the HCP interaction. Return only JSON.

JSON schema:
{{
  "interest_level": "Low|Medium|High",
  "objections_or_concerns": [],
  "product_interest": [],
  "potential_opportunity": "short opportunity statement",
  "evidence": "short evidence from the notes"
}}

Interaction:
{content}
"""

EDIT_EXTRACTION_PROMPT = """
Convert this conversational edit request into JSON fields for the CRM interaction record.
Return only the fields that should change. Dates must be ISO 8601.

Allowed field names:
hcp_name, hcp_specialty, organization, interaction_type, interaction_datetime,
discussion_summary, products_discussed, samples_requested, follow_up_required,
follow_up_date, representative_notes, sentiment, priority, ai_summary,
next_best_action.

Current record:
{current_record}

Edit request:
{edit_request}
"""
