import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [], 
  isLoading: true, 
};

export const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    // Add a new message
    addMessage: (state, action) => {
      // action.payload: { type: 'user' | 'ai', text: string }
      state.messages.push(action.payload);
    },

    // Replace all messages
    setMessages: (state, action) => {
      state.messages = action.payload; // array of messages
    },

    // Clear all messages
    clearMessages: (state) => {
      state.messages = [];
    },

    // Set loading state
    setLoading: (state, action) => {
      state.isLoading = action.payload; // boolean
    },
  },
});

// Export actions
export const { addMessage, setMessages, clearMessages, setLoading } =
  chatSlice.actions;

// Export reducer
export default chatSlice.reducer;
