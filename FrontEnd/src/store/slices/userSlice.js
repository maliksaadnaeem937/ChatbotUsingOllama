import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  name: "",
  email: "",
  userId: "",
  isLoading:true,
};

export const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser: (state, action) => {
      // action.payload should be an object { name, email, userId }
      state.name = action.payload.name;
      state.email = action.payload.email;
      state.userId = action.payload.userId;
      state.isLoading = false;
    },
    clearUser: (state) => {
      state.name = "";
      state.email = "";
      state.userId = "";
      state.isLoading = false;
    }
  }
});

// Export actions
export const { setUser, clearUser } = userSlice.actions;

// Export reducer
export default userSlice.reducer;
