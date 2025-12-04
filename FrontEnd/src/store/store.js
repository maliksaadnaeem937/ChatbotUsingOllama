import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./slices/userSlice";
import chatReducer from "./slices/chatSlice";
import { apiSlice } from "./slices/apiSlice";

export const store = configureStore({
  reducer: {
    user: userReducer,
    chat: chatReducer,
    [apiSlice.reducerPath]: apiSlice.reducer, 
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware), 
});
