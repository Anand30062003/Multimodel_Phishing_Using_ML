import React, { useState } from "react";
import { checkPhishing } from "../services/api";
import ResultBox from "./ResultBox";



function PhishingChecker() {
  const [url, setUrl] = useState("");
  const [text, setText] = useState("");
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const response = await checkPhishing(url, text, image);
    setResult(response);
    setLoading(false);
  };

  return (  
      <div className="container">
        <form onSubmit={handleSubmit}>
          <label>URL</label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
          />

          <label>Text Message</label>
          <textarea
            rows="4"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste email or message here"
          />

          <label>Upload Image</label>
          <input type="file" onChange={(e) => setImage(e.target.files[0])} />

          <button type="submit">
            {loading ? "Analyzing..." : "Check"}
          </button>
        </form>

        {result && <ResultBox result={result} />}
      </div>  
  );
}

export default PhishingChecker;
