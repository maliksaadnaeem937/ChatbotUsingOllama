import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:8000" }),
  endpoints: (builder) => ({
    askAI: builder.mutation({
      query: ({ query, userId }) => ({
        url: "/ask-llm",
        method: "POST",
        body: { query, userId },
      }),
    }),

    // Fetch previous chats automatically (query)
    fetchChats: builder.query({
      query: (userId) => ({
        url: "/get-chats",
        method: "POST",   // still POST
        body: { userId },
      }),
    }),
  }),
});

// Export hooks
export const { useAskAIMutation, useFetchChatsQuery } = apiSlice;
