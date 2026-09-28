import { useState } from "react";

function App() {

  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");


  // Upload PDF
  const uploadPDF = async () => {

    if (!file) {
      alert("Please select a PDF");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    setUploadMessage("Processing PDF...");

    const response = await fetch(
      "http://127.0.0.1:8000/upload",
      {
        method: "POST",
        body: formData
      }
    );

    const data = await response.json();

    setUploadMessage(data.message);
  };


  // Ask question
  const askQuestion = async () => {

    if (!question) {
      return;
    }

    setLoading(true);
    setAnswer("");

    const response = await fetch(
      "http://127.0.0.1:8000/ask",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          question: question
        })
      }
    );

    const data = await response.json();

    setAnswer(data.answer);

    setLoading(false);
  };


  return (

    <div style={{
      width: "700px",
      margin: "50px auto",
      fontFamily: "Arial"
    }}>

      <h1>📄 RAG Document Chat</h1>


      {/* PDF Upload */}

      <div>

        <h3>Upload PDF</h3>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            setFile(e.target.files[0]);
          }}
        />

        <button
          onClick={uploadPDF}
          style={{
            marginLeft: "10px"
          }}
        >
          Upload
        </button>

      </div>


      <p>{uploadMessage}</p>


      {/* Question */}

      <div style={{
        marginTop: "40px"
      }}>

        <h3>Ask Question</h3>

        <input
          type="text"
          value={question}
          placeholder="Ask something about your PDF..."
          onChange={(e) => {
            setQuestion(e.target.value);
          }}
          style={{
            width: "500px",
            padding: "10px"
          }}
        />

        <button
          onClick={askQuestion}
          style={{
            marginLeft: "10px",
            padding: "10px"
          }}
        >
          Ask
        </button>

      </div>


      {/* Answer */}

      <div style={{
        marginTop: "30px"
      }}>

        {loading && <p>🤖 Thinking...</p>}

        {answer && (

          <div>

            <h3>Answer</h3>

            <p>{answer}</p>

          </div>

        )}

      </div>

    </div>
  );
}

export default App;