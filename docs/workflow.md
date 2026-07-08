# Workflow Documentation

## Structured Form Workflow

1. Representative opens Log Interaction.
2. Representative selects Form mode.
3. Representative enters HCP name, specialty, organization, interaction type, date/time, summary, products, samples, follow-up, notes, sentiment, and priority.
4. Frontend validates required browser fields.
5. Backend validates the Pydantic schema.
6. Interaction is saved in Neon PostgreSQL.
7. Dashboard and Interactions screens show the saved record.

## Conversational AI Workflow

1. Representative switches to AI chat mode.
2. Representative types a natural language interaction description.
3. Frontend calls `/api/agent/chat`.
4. LangGraph classifies the intent.
5. LangGraph extracts structured interaction fields with LangChain and Groq.
6. LangGraph validates missing required fields.
7. Frontend shows an editable draft.
8. Representative reviews, edits, and saves the draft.
9. Backend saves the reviewed record through the standard CRUD endpoint.

## LangGraph Workflow

Graph nodes:

- `receive_user_input`
- `classify_intent`
- `extract_interaction_data`
- `validate_data`
- `call_required_tool`
- `generate_response`

Routing:

- Chat log intent routes to extraction and draft response.
- Tool endpoints provide an explicit intent and route directly to the required tool.
- Unknown intent returns a clean JSON message explaining supported actions.

## Tool Execution Workflow

Log Interaction:

1. Accepts structured data or raw text.
2. Extracts missing fields from raw text.
3. Validates required fields.
4. Generates summary, insights, and follow-up recommendation.
5. Saves to Neon PostgreSQL.

Edit Interaction:

1. Accepts interaction ID.
2. Accepts structured updates or conversational edit text.
3. Converts conversational edits into fields when needed.
4. Updates the Neon PostgreSQL record.

Summarize Interaction:

1. Accepts raw notes or interaction ID.
2. Generates concise CRM summary.
3. Stores the summary when an interaction ID is provided.

Suggest Follow-up:

1. Accepts saved interaction or structured data.
2. Reviews sentiment, priority, discussion, and sample request.
3. Returns next best action, urgency, date, and rationale.

Extract HCP Insights:

1. Accepts saved interaction, structured data, or raw notes.
2. Extracts interest level, concerns, product interest, opportunity, and evidence.
3. Stores insights when an interaction ID is provided.

## Query Workflow

1. Client calls `GET /api/interactions/query`.
2. Client may pass free text through `q`, exact filters such as `priority` or `sentiment`, date range filters, follow-up filters, sort fields, and pagination values.
3. FastAPI validates query parameter types and allowed enum values before the service runs.
4. `InteractionService.query()` builds the database query incrementally, adding only filters that were provided.
5. The service counts total matching rows before applying pagination.
6. The service sorts and returns the requested page of results.
7. The API response includes metadata and records: `total`, `count`, `limit`, `offset`, and `items`.
