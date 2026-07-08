# REST API Documentation

## Overview

The backend exposes two REST groups under `/api`:

- Interaction endpoints for database CRUD and querying
- Agent endpoints for Groq/LangGraph-powered AI actions

Interaction endpoints use FastAPI, Pydantic validation, SQLAlchemy, and Neon PostgreSQL. They do not require `GROQ_API_KEY`.

Agent endpoints use the LangGraph workflow and LangChain tools. They require `GROQ_API_KEY`; if it is missing, the API returns HTTP `503` with a clear configuration message.

## Interaction CRUD APIs

### Create Interaction

`POST /api/interactions`

Creates one interaction record.

Request body:

```json
{
  "hcp_name": "Dr. Meera Rao",
  "hcp_specialty": "Cardiology",
  "organization": "City Heart Clinic",
  "interaction_type": "Meeting",
  "interaction_datetime": "2026-07-08T10:30:00",
  "discussion_summary": "Discussed CardioPlus and trial outcomes.",
  "products_discussed": "CardioPlus",
  "samples_requested": "Starter samples",
  "follow_up_required": true,
  "follow_up_date": "2026-07-15T10:00:00",
  "representative_notes": "Doctor asked for trial data.",
  "sentiment": "Positive",
  "priority": "High"
}
```

Response: `201 Created` with the saved interaction, including `id`, `created_at`, and `updated_at`.

### List Interactions

`GET /api/interactions`

Returns all interactions ordered by newest `created_at` first. Use this for simple dashboard/list loading.

Response:

```json
[
  {
    "id": 1,
    "hcp_name": "Dr. Meera Rao",
    "interaction_type": "Meeting",
    "interaction_datetime": "2026-07-08T10:30:00",
    "discussion_summary": "Discussed CardioPlus and trial outcomes.",
    "follow_up_required": true,
    "sentiment": "Positive",
    "priority": "High",
    "created_at": "2026-07-08T10:40:00",
    "updated_at": "2026-07-08T10:40:00"
  }
]
```

### Query Interactions

`GET /api/interactions/query`

This is the new query method. It searches and filters saved interactions in Neon PostgreSQL without involving the LLM.

How it works:

1. FastAPI validates query parameters, including enum values and pagination bounds.
2. `InteractionService.query()` starts from the `interactions` SQLAlchemy model.
3. Optional filters are added only when parameters are present.
4. Free-text `q` uses case-insensitive SQL `ILIKE` across important text columns.
5. The service counts all matching rows before pagination.
6. Sorting, `offset`, and `limit` are applied.
7. The response returns pagination metadata plus the current page of items.

Supported parameters:

| Parameter | Type | Behavior |
| --- | --- | --- |
| `q` | string | Partial, case-insensitive search across HCP name, specialty, organization, summary, products, samples, notes, AI summary, and next best action |
| `hcp_name` | string | Partial, case-insensitive HCP name filter |
| `organization` | string | Partial, case-insensitive organization filter |
| `interaction_type` | enum | Exact match: `Meeting`, `Call`, `Email`, `Conference`, `Follow-up`, `Other` |
| `sentiment` | enum | Exact match: `Positive`, `Neutral`, `Negative` |
| `priority` | enum | Exact match: `Low`, `Medium`, `High` |
| `follow_up_required` | boolean | Filters records where follow-up is required or not required |
| `follow_up_due` | boolean | When `true`, returns records with required follow-up dates at or before current UTC time |
| `date_from` | ISO datetime | Includes records with `interaction_datetime >= date_from` |
| `date_to` | ISO datetime | Includes records with `interaction_datetime <= date_to` |
| `limit` | integer | Page size, default `50`, maximum `100` |
| `offset` | integer | Number of matching rows to skip, default `0` |
| `sort_by` | enum | `created_at`, `updated_at`, `interaction_datetime`, `hcp_name`, `priority`, `sentiment`, `follow_up_date` |
| `sort_order` | enum | `asc` or `desc`, default `desc` |

Example request:

```text
GET /api/interactions/query?q=CardioPlus&priority=High&follow_up_due=true&limit=10&offset=0&sort_by=follow_up_date&sort_order=asc
```

Example response:

```json
{
  "total": 2,
  "count": 2,
  "limit": 10,
  "offset": 0,
  "items": [
    {
      "id": 7,
      "hcp_name": "Dr. Meera Rao",
      "hcp_specialty": "Cardiology",
      "organization": "City Heart Clinic",
      "interaction_type": "Meeting",
      "interaction_datetime": "2026-07-08T10:30:00",
      "discussion_summary": "Discussed CardioPlus and trial outcomes.",
      "products_discussed": "CardioPlus",
      "samples_requested": "Starter samples",
      "follow_up_required": true,
      "follow_up_date": "2026-07-09T10:00:00",
      "representative_notes": "Doctor asked for trial data.",
      "sentiment": "Positive",
      "priority": "High",
      "ai_summary": null,
      "ai_insights": null,
      "next_best_action": null,
      "created_at": "2026-07-08T10:40:00",
      "updated_at": "2026-07-08T10:40:00"
    }
  ]
}
```

Frontend helper:

```js
interactionApi.query({
  q: "CardioPlus",
  priority: "High",
  follow_up_due: true,
  limit: 10,
  sort_by: "follow_up_date",
  sort_order: "asc",
});
```

### Get Interaction

`GET /api/interactions/{id}`

Returns a single interaction by numeric ID. Missing IDs return `404`.

### Update Interaction

`PUT /api/interactions/{id}`

Updates any provided interaction fields. Fields omitted from the request are left unchanged.

### Delete Interaction

`DELETE /api/interactions/{id}`

Deletes a single interaction. Success returns `204 No Content`.

## Agent APIs

### Chat

`POST /api/agent/chat`

Classifies natural language, extracts an editable interaction draft, and returns it to the frontend. This does not save automatically.

### Log Interaction Tool

`POST /api/agent/log-interaction`

Runs the LangGraph log tool. It can extract from raw text, generate summary/insights/follow-up, and save a completed interaction.

### Edit Interaction Tool

`POST /api/agent/edit-interaction`

Updates a saved interaction from structured `updates` or a natural language edit request.

### Summarize Tool

`POST /api/agent/summarize`

Generates a concise CRM summary from raw notes or an existing interaction.

### Suggest Follow-up Tool

`POST /api/agent/suggest-followup`

Returns next best action, urgency, suggested follow-up date, and rationale.

### Extract Insights Tool

`POST /api/agent/extract-insights`

Extracts interest level, objections, product interest, opportunity, and supporting evidence.

## Health API

`GET /api/health`

Returns backend status, app name, and whether Groq is configured.
