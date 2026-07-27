import { useEffect, useState } from "react";
import API from "./services/api";

import Navbar from "./components/Navbar/Navbar";
import SessionSidebar from "./components/Sessions/SessionSidebar";
import Sidebar from "./components/Sidebar/Sidebar";
import UploadBox from "./components/Upload/UploadBox";
import ChatWindow from "./components/Chat/ChatWindow";

function App() {

  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);

  // NEW
  const [sessions, setSessions] = useState([]);
  const [currentSession, setCurrentSession] = useState(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {

    try {

      const response = await API.get("/files");

      setDocuments(response.data.documents);

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <div className="h-screen flex flex-col">

      <Navbar />

      <div className="flex flex-1">

        {/* Chat Sessions */}
        <SessionSidebar
          sessions={sessions}
          setSessions={setSessions}
          currentSession={currentSession}
          setCurrentSession={setCurrentSession}
          messages={messages}
          setMessages={setMessages}
        />

        {/* Uploaded Documents */}
        <Sidebar
          documents={documents}
          setDocuments={setDocuments}
        />

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">

          <UploadBox
            setDocuments={setDocuments}
          />

          <ChatWindow
            messages={messages}
            setMessages={setMessages}
            currentSession={currentSession}
          />

        </div>

      </div>

    </div>

  );

}

export default App;