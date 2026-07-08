# Architecture

## System Architecture

The project is a three-layer local application:

- React frontend for CRM workflows and tool demos
- FastAPI backend for REST APIs, validation, LangGraph orchestration, and persistence
- Neon-hosted PostgreSQL database for interaction records

The frontend talks to the backend through JSON APIs under `/api`. The backend uses SQLAlchemy with a `DATABASE_URL` environment variable for database access and LangGraph/LangChain/Groq for AI workflows.

## Frontend Architecture

React is organized by feature:

- `features/interactions`: Redux thunks and slice for CRUD operations
- `features/interactions/interactionApi.js`: CRUD calls plus the query helper for filtered searches
- `features/agent`: Redux thunks and slice for AI chat and tool endpoints
- `components`: reusable CRM layout, form, chat logger, lists, details, and tool panel
- `pages`: dashboard, log interaction, and interactions management

Redux Toolkit owns API request state, errors, saved interactions, chat messages, and AI drafts.

## Backend Architecture

FastAPI is organized into:

- `models`: SQLAlchemy interaction table model
- `schemas`: Pydantic request/response models
- `services`: database CRUD service and LangChain/Groq service
- `routes`: REST and agent endpoints
- `agents`: LangGraph workflow, LangChain prompts, and tools

Manual CRUD endpoints do not require an LLM key. Agent endpoints require `GROQ_API_KEY` and return a clear 503 when it is missing.

The interaction route group also exposes `GET /api/interactions/query` for database-side searching, filtering, sorting, and pagination.

## LangGraph Architecture

`HCPAgent` builds a LangGraph state machine with these nodes:

- `receive_user_input`: normalizes message and conversation context
- `classify_intent`: classifies intent using Groq through LangChain
- `extract_interaction_data`: extracts structured CRM fields from natural language
- `validate_data`: checks required fields
- `call_required_tool`: invokes the selected LangChain `StructuredTool`
- `generate_response`: returns frontend-ready JSON

The graph routes intents to:

- `log_interaction`
- `edit_interaction`
- `summarize_interaction`
- `suggest_followup`
- `extract_insights`
- `unknown`

## Database Architecture

Primary table: `interactions`

Important columns:

- HCP details: `hcp_name`, `hcp_specialty`, `organization`
- Interaction details: `interaction_type`, `interaction_datetime`, `discussion_summary`
- Business fields: `products_discussed`, `samples_requested`, `follow_up_required`, `follow_up_date`
- CRM prioritization: `sentiment`, `priority`
- AI outputs: `ai_summary`, `ai_insights`, `next_best_action`
- Audit fields: `created_at`, `updated_at`

## Request/Response Flow

Structured form:

1. User completes React form.
2. Redux dispatches `POST /api/interactions`.
3. FastAPI validates with Pydantic.
4. SQLAlchemy saves to Neon PostgreSQL.
5. Frontend refreshes state and shows success.

AI chat:

1. User sends natural language text.
2. Redux dispatches `POST /api/agent/chat`.
3. LangGraph classifies intent and extracts a draft.
4. Frontend displays editable draft.
5. User saves reviewed draft through `POST /api/interactions`.

Tool execution:

1. User clicks a tool button.
2. Frontend calls the matching `/api/agent/*` endpoint.
3. LangGraph routes to the selected LangChain tool.
4. Tool uses Groq and/or database service.
5. API returns structured JSON to the tool panel.

Query method:

1. Client calls `GET /api/interactions/query` with query-string filters.
2. FastAPI validates query parameters and enum values.
3. `InteractionService.query()` builds a SQLAlchemy query against `interactions`.
4. Free-text search uses case-insensitive matching across key CRM text fields.
5. Exact filters, date range filters, follow-up due logic, sorting, and pagination are applied.
6. API returns `{ total, count, limit, offset, items }`.
