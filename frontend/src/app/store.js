import { configureStore } from "@reduxjs/toolkit";
import agentReducer from "../features/agent/agentSlice";
import interactionsReducer from "../features/interactions/interactionSlice";

export const store = configureStore({
  reducer: {
    interactions: interactionsReducer,
    agent: agentReducer,
  },
});
