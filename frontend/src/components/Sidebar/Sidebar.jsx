import API from "../../services/api";

function Sidebar({ documents, setDocuments }) {

  const deleteDocument = async (filename) => {

    try {

      await API.delete(`/document/${filename}`);

      setDocuments(
        documents.filter(doc => doc !== filename)
      );

    } catch (error) {

      console.error(error);

    }

  };

  const clearAll = async () => {

    try {

      await API.delete("/files");

      setDocuments([]);

    } catch (error) {

      console.error(error);

    }

  };

  return (

    <div className="w-72 bg-white border-r p-4">

      <h2 className="text-xl font-bold mb-4">
        📄 Uploaded Documents
      </h2>

      {
        documents.length === 0 ?

        <div className="text-gray-500">
          No documents uploaded
        </div>

        :

        <>

          {documents.map((doc, index) => (

            <div
              key={index}
              className="flex justify-between items-center bg-gray-100 p-2 rounded mb-2"
            >

              <span className="text-sm truncate">
                📄 {doc}
              </span>

              <button
                onClick={() => deleteDocument(doc)}
                className="text-red-600 hover:text-red-800"
              >
                🗑
              </button>

            </div>

          ))}

          <button
            onClick={clearAll}
            className="mt-4 w-full bg-red-600 text-white p-2 rounded"
          >
            Clear All
          </button>

        </>

      }

    </div>

  );

}

export default Sidebar;