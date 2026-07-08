import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { interactionApi } from "./interactionApi";

export const fetchInteractions = createAsyncThunk("interactions/fetchAll", interactionApi.list);
export const createInteraction = createAsyncThunk("interactions/create", interactionApi.create);
export const updateInteraction = createAsyncThunk(
  "interactions/update",
  ({ id, data }) => interactionApi.update(id, data)
);
export const deleteInteraction = createAsyncThunk("interactions/delete", async (id) => {
  await interactionApi.remove(id);
  return id;
});

const interactionSlice = createSlice({
  name: "interactions",
  initialState: {
    items: [],
    selectedId: null,
    status: "idle",
    error: null,
    success: null,
  },
  reducers: {
    selectInteraction: (state, action) => {
      state.selectedId = action.payload;
    },
    clearInteractionMessages: (state) => {
      state.error = null;
      state.success = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
        if (!state.selectedId && action.payload.length) state.selectedId = action.payload[0].id;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.items.unshift(action.payload);
        state.selectedId = action.payload.id;
        state.success = "Interaction saved.";
      })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        state.items = state.items.map((item) => (item.id === action.payload.id ? action.payload : item));
        state.success = "Interaction updated.";
      })
      .addCase(deleteInteraction.fulfilled, (state, action) => {
        state.items = state.items.filter((item) => item.id !== action.payload);
        if (state.selectedId === action.payload) state.selectedId = state.items[0]?.id || null;
        state.success = "Interaction deleted.";
      })
      .addMatcher(
        (action) => action.type.startsWith("interactions/") && action.type.endsWith("/pending"),
        (state) => {
          state.status = "loading";
          state.error = null;
        }
      )
      .addMatcher(
        (action) => action.type.startsWith("interactions/") && action.type.endsWith("/rejected"),
        (state, action) => {
          state.status = "failed";
          state.error = action.error.message;
        }
      );
  },
});

export const { selectInteraction, clearInteractionMessages } = interactionSlice.actions;
export default interactionSlice.reducer;
