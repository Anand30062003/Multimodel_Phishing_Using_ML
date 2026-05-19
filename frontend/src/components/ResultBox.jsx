import React from "react";

function ResultBox({ result }) {
  return (
    <div className="result-box">
      <h3>Detection Result</h3>
      <p><b>Status:</b> {result.result}</p>
      <p><b>Risk Score:</b> {result.score}%</p>
      <p><b>Message:</b> {result.message}</p>
    </div>
  );
}

export default ResultBox;
