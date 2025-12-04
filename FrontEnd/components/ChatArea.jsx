import { Bot, User } from "lucide-react";
import { useSelector } from "react-redux";

export default function ChatArea() {
  const {messages}=useSelector((state)=>state.chat)


  return (
    <div className="flex flex-col space-y-4">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`flex items-start space-x-3 ${
            msg.type === "user" ? "justify-end" : "justify-start"
          }`}
        >
          {msg.type === "ai" && <Bot className="text-white h-8 w-8" />}

          <div
            className={`max-w-[75%] px-4 py-3 text-white rounded-2xl break-words ${
              msg.type === "user"
                ? "bg-blue-600 rounded-br-none"
                : "bg-gray-700 rounded-bl-none"
            }`}
          >
            {msg.text}
          </div>

          {msg.type === "user" && <User className="text-white h-8 w-8" />}
        </div>
      ))}
    </div>
  );
}
