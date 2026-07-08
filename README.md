# AI-First CRM HCP Module - Log Interaction Screen

Submission-ready Round 1 technical assignment project for logging Healthcare Professional interactions using a structured CRM form or a conversational AI workflow.

## Objective

Build an AI-first CRM module for life sciences field representatives. The app captures HCP interactions, extracts structured data from natural language, saves records to Neon PostgreSQL, and exposes five LangGraph/LangChain tools powered by Groq `gemma2-9b-it`.

## Tech Stack

- Frontend: React, Redux Toolkit, Vite, React Router, Lucide icons, Google Inter
- Backend: Python FastAPI, SQLAlchemy ORM, Pydantic
- AI workflow: LangGraph plus LangChain prompt chains and LangChain tools
- LLM provider: Groq
- Required model: `gemma2-9b-it`
- Optional context model setting: `llama-3.3-70b-versatile`
- Database: Neon PostgreSQL via `DATABASE_URL`

## Features

- Structured HCP interaction form with validation
- Conversational AI chat logger that extracts an editable draft
- CRUD screen for saved interactions
- Dashboard metrics for total interactions, follow-ups due, high priority HCPs, and recent records
- Tool demo panel for all five LangGraph tools
- Clear missing `GROQ_API_KEY` errors instead of crashes
- Neon PostgreSQL-backed persistence through SQLAlchemy

## LangGraph Agent

The backend builds a real LangGraph `StateGraph` in `backend/app/agents/graph.py`.

Workflow nodes:

1. `receive_user_input`
2. `classify_intent`
3. `extract_interaction_data`
4. `validate_data`
5. `call_required_tool`
6. `generate_response`

LangChain is used for prompt templates, Groq chat model calls, JSON parsing, text parsing, and `StructuredTool` wrappers. AI endpoints require a valid `GROQ_API_KEY`.

## Implemented LangGraph Tools

- Log Interaction: extracts/enriches data, summarizes notes, extracts insights, suggests follow-up, validates, and saves to DB
- Edit Interaction: updates a saved interaction from structured fields or conversational edit text
- Summarize Interaction: creates a concise CRM-friendly summary
- Suggest Follow-up: recommends next best action, urgency, date, and rationale
- Extract HCP Insights: extracts interest level, objections, product interest, opportunity, and evidence

## Folder Structure

```text
backend/
  app/
    agents/
    docs/
    models/
    routes/
    schemas/
    services/
    main.py
  requirements.txt
  .env.example
frontend/
  src/
    app/
    components/
    features/
    pages/
    styles/
  package.json
  .env.example
docs/
  architecture.md
  rest-api.md
  workflow.md
  usecases.md
README.md
```

## Neon PostgreSQL Setup

Create a Neon project and copy the pooled or direct PostgreSQL connection string from the Neon dashboard. The URL should include SSL:

```text
postgresql://user:password@host.neon.tech/database?sslmode=require
```

Tables are created automatically when FastAPI starts.

## Backend Setup

Use Python 3.10 or newer. On Windows, `py -3.10` is a safe choice if the default `python` command points to an older interpreter.

```bash
cd backend
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `backend/.env` and set:

```text
DATABASE_URL=postgresql://your_neon_user:your_neon_password@your-neon-host.neon.tech/your_database?sslmode=require
GROQ_API_KEY=your_groq_api_key_here
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

## Frontend Setup

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## API Endpoints

Interactions:

- `POST /api/interactions`
- `GET /api/interactions`
- `GET /api/interactions/query`
- `GET /api/interactions/{id}`
- `PUT /api/interactions/{id}`
- `DELETE /api/interactions/{id}`

Query method:

`GET /api/interactions/query` searches saved interactions directly in Neon PostgreSQL. It does not call Groq or LangGraph.

Common query parameters:

- `q`: free-text search across HCP, organization, discussion, products, samples, notes, AI summary, and next action
- `hcp_name`, `organization`: partial text filters
- `interaction_type`: `Meeting`, `Call`, `Email`, `Conference`, `Follow-up`, or `Other`
- `sentiment`: `Positive`, `Neutral`, or `Negative`
- `priority`: `Low`, `Medium`, or `High`
- `follow_up_required`: `true` or `false`
- `follow_up_due`: `true` to return only due follow-ups
- `date_from`, `date_to`: ISO datetime range for `interaction_datetime`
- `limit`, `offset`: pagination, default `50` and `0`
- `sort_by`, `sort_order`: sort field and `asc` or `desc`

Example:

```text
GET /api/interactions/query?q=CardioPlus&priority=High&follow_up_due=true&limit=10&sort_by=follow_up_date&sort_order=asc
```

Detailed REST documentation is in `docs/rest-api.md`.

Agent and tools:

- `POST /api/agent/chat`
- `POST /api/agent/log-interaction`
- `POST /api/agent/edit-interaction`
- `POST /api/agent/summarize`
- `POST /api/agent/suggest-followup`
- `POST /api/agent/extract-insights`

Health:

- `GET /api/health`

## Demo Workflow

1. Create/configure the Neon database, then start the backend and frontend.
2. Open Dashboard and show empty state or existing metrics.
3. Go to Log Interaction and save a structured form entry.
4. Switch to AI chat mode and paste: “Met Dr. Sharma today at Apollo Hospital. Discussed CardioPlus. He seemed positive and asked for samples. Follow up next Monday.”
5. Review/edit the extracted draft and save it.
6. Open Interactions, view details, edit a record, and delete a record if desired.
7. Return to Dashboard and use the Tool Demo Panel:
   - Log Interaction
   - Edit Interaction
   - Summarize
   - Suggest Follow-up
   - Extract Insights

## Video Recording Guide

For a 10-15 minute walkthrough:

1. Show project structure and `.env.example` files.
2. Show `DATABASE_URL` configured in `backend/.env` without exposing the password.
3. Start backend and open `/docs`.
4. Start frontend and show dashboard.
5. Demonstrate structured form save.
6. Demonstrate AI chat extraction, review, edit, save.
7. Demonstrate all five LangGraph tools from the dashboard panel.
8. Show the saved interaction in Neon PostgreSQL-backed UI.
9. Briefly open `backend/app/agents/hcp_agent.py`, `tools.py`, and `graph.py`.
10. Mention missing API key behavior: AI endpoints return a clear 503 message.

## Screenshots

Add screenshots after running locally:

- Dashboard
- Structured form mode
- AI chat draft extraction
- Interactions detail/edit screen
- LangGraph tool demo panel

## Future Improvements

- Authentication and role-based access for field teams
- HCP master data search
- Compliance review tool for regulated claims
- Visit planning and territory optimization
- Alembic migrations for production schema management
- Automated frontend and backend test suites
"# HCP-CRM" 
