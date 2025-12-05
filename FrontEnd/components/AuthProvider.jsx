"use client";

import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { setUser, clearUser } from "@/store/slices/userSlice";
import { onAuthStateChangedListener } from "@/utils/auth-listener";

export default function AuthProvider({ children }) {
  const dispatch = useDispatch();


  useEffect(() => {
    const unsubscribe = onAuthStateChangedListener((user) => {
      if (user) {
        dispatch(
          setUser({
            name: user?.displayName || "",
            email: user?.email || "",
            userId: user?.uid||"",
          })
        );
      } else {
        dispatch(clearUser());
      }
    });

    return () => unsubscribe();
  }, [dispatch]);

  return <>{children}</>;
}
