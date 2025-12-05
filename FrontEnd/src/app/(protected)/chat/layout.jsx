"use client";
import { useFetchChatsQuery } from "@/store/slices/apiSlice";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useRef } from "react";
import { setMessages } from "@/store/slices/chatSlice";
import ChatArea from "../../../../components/ChatArea";
export default function ChatLoader({ children }) {
  const dispatch = useDispatch();
  const { userId } = useSelector((state) => state.user);
  const {
    data,
    isLoading: loadingChatFirstTime,
    error,
  } = useFetchChatsQuery(userId);

  const { messages } = useSelector((state) => state.chat);

  const chatRef = useRef(null);
  useEffect(() => {
    if (data) {
      dispatch(setMessages(data?.messages || []));
    }
  }, [data]);
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="w-full h-screen bg-gray-800 relative flex flex-col">
      <div ref={chatRef} className="flex-1 overflow-y-auto p-6 mb-24">
        {!loadingChatFirstTime ? (
          <ChatArea />
        ) : (
          <div className="text-3xl text-center text-white">
            Loading Prev Chats
          </div>
        )}
      </div>
      {children}
    </div>
  );
}
