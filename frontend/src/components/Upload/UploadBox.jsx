import { useState } from "react";
import API from "../../services/api";

function UploadBox({ setDocuments }) {
  const [file, setFile] = useState(null);

  const uploadPDF = async () => {
    if (!file) {
      alert("Please select a PDF.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await API.post(
        "/document/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Add uploaded file to sidebar
      setDocuments((prev) => [...prev, response.data.filename]);

      alert("PDF uploaded successfully!");

      // Clear selected file
      setFile(null);

      // Clear file input
      document.getElementById("pdfFile").value = "";

    } catch (error) {
      console.error(error);

      if (error.response?.data?.error) {
        alert(error.response.data.error);
      } else {
        alert("Upload failed.");
      }
    }
  };

  return (
    <div className="p-4 border-b">

      <input
        id="pdfFile"
        type="file"
        accept=".pdf,.docx,.txt,.md,.html,.htm,.pptx,.xlsx,.xls,.csv"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-3 w-full"
      />

      <button
        onClick={uploadPDF}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Upload Document
      </button>

    </div>
  );
}

export default UploadBox;