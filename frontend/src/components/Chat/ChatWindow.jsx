import { useEffect, useRef } from "react";

import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

function ChatWindow({
  messages,
  setMessages,
  currentSession,
}) {

  const bottomRef = useRef(null);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);

  return (

    <div className="flex-1 flex flex-col bg-gray-50">

      <div className="flex-1 overflow-y-auto p-6">

        {messages.length === 0 ? (

          <div className="text-center text-gray-500 mt-20">

            👋 Upload a PDF and ask your first question.

          </div>

        ) : (

          messages.map((msg, index) => (

            <ChatMessage
              key={index}
              role={msg.role}
              content={msg.content}
              sources={msg.sources}
            />

          ))

        )}

        {/* Auto Scroll Target */}
        <div ref={bottomRef}></div>

      </div>

      <ChatInput
        messages={messages}
        setMessages={setMessages}
        currentSession={currentSession}
      />

    </div>

  );

}

export default ChatWindow;