import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { agentApi } from "./agentApi";

export const sendChatMessage = createAsyncThunk("agent/chat", agentApi.chat);
export const runLogTool = createAsyncThunk("agent/logTool", agentApi.logInteraction);
export const runEditTool = createAsyncThunk("agent/editTool", agentApi.editInteraction);
export const runSummaryTool = createAsyncThunk("agent/summaryTool", agentApi.summarize);
export const runFollowupTool = createAsyncThunk("agent/followupTool", agentApi.suggestFollowup);
export const runInsightsTool = createAsyncThunk("agent/insightsTool", agentApi.extractInsights);

const agentSlice = createSlice({
  name: "agent",
  initialState: {
    chatMessages: [],
    draft: null,
    toolResult: null,
    status: "idle",
    error: null,
  },
  reducers: {
    clearAgentError: (state) => {
      state.error = null;
    },
    updateDraftField: (state, action) => {
      if (!state.draft) state.draft = {};
      state.draft[action.payload.name] = action.payload.value;
    },
    clearDraft: (state) => {
      state.draft = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendChatMessage.pending, (state, action) => {
        state.status = "loading";
        state.error = null;
        state.chatMessages.push({ role: "user", content: action.meta.arg.message });
      })
      .addCase(sendChatMessage.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.draft = action.payload.data?.draft || null;
        state.chatMessages.push({ role: "assistant", content: action.payload.message });
      })
      .addMatcher(
        (action) => action.type.startsWith("agent/") && action.type.endsWith("/pending") && action.type !== sendChatMessage.pending.type,
        (state) => {
          state.status = "loading";
          state.error = null;
        }
      )
      .addMatcher(
        (action) => action.type.startsWith("agent/") && action.type.endsWith("/fulfilled") && action.type !== sendChatMessage.fulfilled.type,
        (state, action) => {
          state.status = "succeeded";
          state.toolResult = action.payload;
        }
      )
      .addMatcher(
        (action) => action.type.startsWith("agent/") && action.type.endsWith("/rejected"),
        (state, action) => {
          state.status = "failed";
          state.error = action.error.message;
          if (action.meta?.arg?.message) {
            state.chatMessages.push({ role: "assistant", content: action.error.message });
          }
        }
      );
  },
});

export const { clearAgentError, updateDraftField, clearDraft } = agentSlice.actions;
export default agentSlice.reducer;
