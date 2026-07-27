import { useState } from "react";

function ChatInput({
  messages,
  setMessages,
  currentSession,
}) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!input.trim() || loading) return;

    if (!currentSession) {
      alert("Please create a chat first.");
      return;
    }

    const question = input;

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    setInput("");

    // Add empty assistant message
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "",
        sources: [],
      },
    ]);

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/chat/stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",

            // Uncomment after authentication is enabled
            // "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            session_id: currentSession.session_id,
            question: question,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Streaming failed");
      }

      const reader = response.body.getReader();

      const decoder = new TextDecoder();

      let fullAnswer = "";

      while (true) {

        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);

        const lines = chunk.split("\n");

        for (const line of lines) {

          if (line.startsWith("data: ")) {

            const token = line.replace("data: ", "");

            fullAnswer += token;

            setMessages((prev) => {

              const updated = [...prev];

              updated[updated.length - 1] = {
                role: "assistant",
                content: fullAnswer,
                sources: [],
              };

              return updated;

          });

        }

      }

      }

    } catch (err) {

      console.error(err);

      setMessages((prev) => {

        const updated = [...prev];

        updated[updated.length - 1] = {
          role: "assistant",
          content: "❌ Server Error",
          sources: [],
        };

        return updated;

      });

    }

    setLoading(false);

  };

  const handleKeyDown = (e) => {

    if (e.key === "Enter" && !e.shiftKey) {

      e.preventDefault();

      sendMessage();

    }

  };

  return (

    <div className="flex p-4 border-t bg-white">

      <input
        type="text"
        className="flex-1 border rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
        placeholder={
          loading
            ? "AI is typing..."
            : "Ask anything about your documents..."
        }
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
      />

      <button
        onClick={sendMessage}
        disabled={loading}
        className="ml-3 bg-blue-600 hover:bg-blue-700 text-white px-5 rounded-lg disabled:bg-gray-400"
      >
        {loading ? "Thinking..." : "Send"}
      </button>

    </div>

  );

}

export default ChatInput;