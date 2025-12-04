"use client";
import { useFetchChatsQuery } from "@/store/slices/apiSlice";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { setMessages } from "@/store/slices/chatSlice";
export default function ChatLoader({ children }) {
  const dispatch = useDispatch();
  const { userId } = useSelector((state) => state.user);
  const { data, isLoading, error } = useFetchChatsQuery(userId);

  useEffect(() => {
    if (data) {
      dispatch(setMessages(data?.messages || []));
    }
  }, [data]);

  return <>{children}</>;
}
