# Use Cases

## Use Case 1: Log Interaction Manually

Actor: Field representative

Flow:

1. Open Log Interaction.
2. Select Form mode.
3. Fill required and optional CRM fields.
4. Save the record.
5. Confirm it appears in Interactions and Dashboard.

Outcome: A validated HCP interaction is stored in Neon PostgreSQL.

## Use Case 2: Log Interaction Through Chat

Actor: Field representative

Flow:

1. Open Log Interaction.
2. Select AI chat mode.
3. Type a natural language interaction note.
4. LangGraph extracts an editable draft.
5. Review and correct fields.
6. Save the draft.

Outcome: A natural language note becomes a structured CRM record.

## Use Case 3: Edit Interaction

Actor: Field representative

Flow:

1. Open Interactions.
2. Select a saved interaction.
3. Click Edit.
4. Modify fields.
5. Save updates.

Outcome: The Neon PostgreSQL record is updated and visible in the UI.

## Use Case 4: Summarize Interaction

Actor: Field representative or manager

Flow:

1. Open Dashboard tool demo panel.
2. Choose a saved interaction or enter raw notes.
3. Click Summarize.

Outcome: LangGraph invokes the summarize tool and returns a concise CRM summary.

## Use Case 5: Suggest Follow-up

Actor: Field representative

Flow:

1. Select a saved interaction or use text-derived sample data.
2. Click Suggest Follow-up.
3. Review next best action, urgency, suggested date, and rationale.

Outcome: Representative receives an actionable follow-up recommendation.

## Use Case 6: Extract HCP Insights

Actor: Field representative or sales manager

Flow:

1. Select a saved interaction or enter raw notes.
2. Click Extract Insights.
3. Review interest level, objections, product interest, opportunity, and evidence.

Outcome: Interaction notes become structured sales insight data.

## Use Case 7: Query Saved Interactions

Actor: Field representative or manager

Flow:

1. A client calls `GET /api/interactions/query`.
2. The client passes filters such as product keyword, HCP name, priority, sentiment, due follow-up, or date range.
3. Backend searches Neon PostgreSQL and returns only matching records.
4. Client uses the `total`, `limit`, and `offset` metadata for pagination.

Outcome: Saved CRM interactions can be searched and filtered without using the AI workflow.
