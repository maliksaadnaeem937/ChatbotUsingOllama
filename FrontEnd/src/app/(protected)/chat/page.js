"use client";
import { useState, useRef, useEffect } from "react";
import ChatArea from "../../../../components/ChatArea"; // separate component
import { useDispatch, useSelector } from "react-redux";
import { addMessage } from "@/store/slices/chatSlice";
import { useAskAIMutation } from "@/store/slices/apiSlice";

export default function Page() {
  const [askAI, { data, isLoading: isAskingAi, error }] = useAskAIMutation();

  const { userId } = useSelector((state) => state.user);

  const [input, setInput] = useState("");
  const dispatch = useDispatch();

  const { messages } = useSelector((state) => state.chat);

  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Dispatch user message
    dispatch(addMessage({ type: "user", text: input }));
    setInput("");

    try {
      const response = await askAI({ query: input, userId: userId }).unwrap();

      dispatch(addMessage(response));
    } catch (error) {
      console.error("Error calling AI:", error);
      dispatch(addMessage({ type: "ai", text: "Oops! Something went wrong." }));
    }
  };

  return (
    <div className="w-full h-screen bg-gray-800 relative flex flex-col">
      <div ref={chatRef} className="flex-1 overflow-y-auto p-6 mb-24">
        <ChatArea  />
      </div>

      {/* INPUT BAR */}
      <div className="w-full p-4 bg-gray-900 fixed bottom-0 left-0">
        <div className="max-w-3xl mx-auto flex items-center space-x-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            className="flex-1 px-4 py-3 bg-gray-800 text-white rounded-2xl border border-gray-700 focus:outline-none focus:border-gray-500"
            placeholder="Message..."
          />
          <button
            onClick={handleSend}
            disabled={isAskingAi}
            className="bg-gray-200 text-black px-4 py-3 rounded-xl font-medium hover:bg-gray-300 transition"
          >
            Ask Ai
          </button>
        </div>
      </div>
    </div>
  );
}
