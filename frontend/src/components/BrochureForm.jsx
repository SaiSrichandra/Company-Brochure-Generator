import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';

const API_BASE_URL = import.meta.env.VITE_API_URL;

function BrochureForm() {
  const [companyName, setCompanyName] = useState('');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [markdown, setMarkdown] = useState('');
  const [progress, setProgress] = useState(0);

  const intervalRef = useRef(null);

  // Simulate progress bar
  const startProgressBar = (estimatedTime = 120000) => {
    const tickRate = 200; // update every 200ms
    const increment = 100 / (estimatedTime / tickRate); // how much to add each tick

    setProgress(0);
    clearInterval(intervalRef.current);

    intervalRef.current = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return 90; // cap progress
        return prev + increment;
      });
    }, tickRate);
  };

  const stopProgressBar = () => {
    clearInterval(intervalRef.current);
    setProgress(100);
    setTimeout(() => setProgress(0), 500); // reset after brief pause
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMarkdown('');
    startProgressBar(125000); // estimate 25s duration

    try {
      const res = await fetch(`${API_BASE_URL}/generate-brochure`, {
        method: "POST",
        headers: {'Content-Type': 'application/json','ngrok-skip-browser-warning': 'true'},
        body: JSON.stringify({ company_name: companyName, url })
      });

      const data = await res.json();
      setMarkdown(data.markdown);
    } catch (err) {
      console.error("Error:", err);
      alert("Something went wrong while generating the brochure.");
    } finally {
      setLoading(false);
      stopProgressBar();
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Company Name"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          required
        />
        <input
          type="url"
          placeholder="Company Website URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Brochure"}
        </button>
      </form>

      <hr />

      {loading && (
        <div className="progress-bar-container">
          <div
            className="progress-bar"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      )}

      {!loading && markdown && (
        <div className="react-markdown">
          <ReactMarkdown>{markdown}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default BrochureForm;
