import { useEffect } from "react";
import API from "../../services/api";

function SessionSidebar({
  sessions,
  setSessions,
  currentSession,
  setCurrentSession,
  messages,
  setMessages,
}) {
  useEffect(() => {
    loadSessions();
  }, []);

  // Load all sessions
  const loadSessions = async () => {
    try {
      const res = await API.get("/session/");

      setSessions(res.data);

      if (res.data.length > 0 && !currentSession) {
        loadSession(res.data[0]);
      }

    } catch (err) {
      console.log(err);
    }
  };

  // Load selected session history
  const loadSession = async (session) => {
    try {

      const res = await API.get(
        `/session/${session.session_id}/history`
      );

      setCurrentSession(session);

      setMessages(res.data);

    } catch (err) {
      console.log(err);
    }
  };

  // Create new chat
  const createSession = async () => {
    try {

      const res = await API.post("/session/new");

      setSessions((prev) => [res.data, ...prev]);

      setCurrentSession(res.data);

      setMessages([]);

    } catch (err) {
      console.log(err);
    }
  };

  // Delete chat
  const deleteSession = async (sessionId) => {
    try {

      await API.delete(`/session/${sessionId}`);

      const updated = sessions.filter(
        (s) => s.session_id !== sessionId
      );

      setSessions(updated);

      if (
        currentSession &&
        currentSession.session_id === sessionId
      ) {

        if (updated.length > 0) {

          loadSession(updated[0]);

        } else {

          setCurrentSession(null);
          setMessages([]);

        }

      }

    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col">

      <button
        onClick={createSession}
        className="m-3 p-3 rounded bg-green-600 hover:bg-green-700"
      >
        + New Chat
      </button>

      <div className="flex-1 overflow-y-auto">

        {sessions.map((session) => (

          <div
            key={session.session_id}
            className={`flex justify-between items-center p-3 cursor-pointer hover:bg-gray-700 ${
              currentSession?.session_id === session.session_id
                ? "bg-gray-700"
                : ""
            }`}
          >

            <span
              className="flex-1"
              onClick={() => loadSession(session)}
            >
              {session.title}
            </span>

            <button
              onClick={() =>
                deleteSession(session.session_id)
              }
            >
              🗑
            </button>

          </div>

        ))}

      </div>

    </div>
  );
}

export default SessionSidebar;