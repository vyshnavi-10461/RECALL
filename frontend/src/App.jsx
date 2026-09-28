import { useState } from "react";
import "./App.css";

function App() {
  const [service, setService] = useState("Payment API");
  const [severity, setSeverity] = useState("critical");
  const [problem, setProblem] = useState(
    "Database connection timeout during peak traffic"
  );

  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const [feedbackLoading, setFeedbackLoading] = useState(false);

  // -----------------------------
  // Analyze Incident
  // -----------------------------

  const analyzeIncident = async () => {
    setLoading(true);
    setAnalysis(null);
    setError("");
    setFeedbackMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/incidents/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            service,
            severity,
            problem,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || data.error) {
        throw new Error(
          data.message || data.error || "Failed to analyze incident"
        );
      }

      setAnalysis(data);
    } catch (error) {
      console.error("Analyze error:", error);

      setError(
        error.message || "Could not connect to the RECALL backend"
      );
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------
  // Send Feedback / Learn
  // -----------------------------

  const sendFeedback = async (outcome) => {
    setFeedbackLoading(true);
    setFeedbackMessage("");
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/incidents/feedback",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            service,
            problem,
            recommended_resolution:
              analysis?.ai_analysis || "No recommendation available",

            engineer_action:
              outcome === "SUCCESSFUL"
                ? "Engineer applied the recommended resolution"
                : "Engineer tried the recommended resolution but it did not resolve the incident",

            outcome,

            recovery_time_minutes:
              outcome === "SUCCESSFUL" ? 5 : 0,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setFeedbackMessage(
          outcome === "SUCCESSFUL"
            ? "✓ Outcome saved. RECALL learned from this incident."
            : "✓ Failure saved. RECALL learned that this resolution did not work."
        );
      } else {
        console.error(data);

        setFeedbackMessage(
          data.detail ||
            data.message ||
            "Something went wrong while saving the outcome."
        );
      }
    } catch (error) {
      console.error(error);

      setFeedbackMessage(
        "Could not connect to the RECALL backend."
      );
    } finally {
      setFeedbackLoading(false);
    }
  };

  // -----------------------------
  // Extract AI Sections
  // -----------------------------

  const getSection = (text, start, end) => {
    const startIndex = text.indexOf(start);

    if (startIndex === -1) {
      return "";
    }

    const contentStart = startIndex + start.length;

    const endIndex = end
      ? text.indexOf(end, contentStart)
      : -1;

    return text
      .slice(
        contentStart,
        endIndex === -1 ? text.length : endIndex
      )
      .trim();
  };

  // -----------------------------
  // Render AI Analysis
  // -----------------------------

  const renderAnalysis = () => {
    if (!analysis) {
      return null;
    }

    const text = analysis.ai_analysis || "";

    const rootCause = getSection(
      text,
      "LIKELY ROOT CAUSE:",
      "RECOMMENDED RESOLUTION:"
    );

    const resolution = getSection(
      text,
      "RECOMMENDED RESOLUTION:",
      "WHY THIS RECOMMENDATION:"
    );

    const why = getSection(
      text,
      "WHY THIS RECOMMENDATION:",
      "HISTORICAL EVIDENCE:"
    );

    const evidence = getSection(
      text,
      "HISTORICAL EVIDENCE:",
      "EXPECTED RECOVERY:"
    );

    const recovery = getSection(
      text,
      "EXPECTED RECOVERY:",
      null
    );

    return (
      <section className="analysis-section">

        {/* Analysis Header */}

        <div className="section-title">
          <div>
            <p className="eyebrow">AI RESPONSE</p>
            <h2>AI Incident Analysis</h2>
          </div>

          <span className="memory-badge">
            🧠 Hindsight Memory
          </span>
        </div>


        {/* Main Analysis Cards */}

        <div className="analysis-grid">

          <div className="analysis-card root-cause-card">
            <div className="card-icon">🔴</div>

            <div>
              <div className="card-label">
                Likely Root Cause
              </div>

              <div className="card-value">
                {rootCause || "No root cause identified"}
              </div>
            </div>
          </div>


          <div className="analysis-card resolution-card">
            <div className="card-icon">🛠️</div>

            <div>
              <div className="card-label">
                Recommended Resolution
              </div>

              <div className="card-value">
                {resolution || "No resolution recommended"}
              </div>
            </div>
          </div>


          <div className="analysis-card why-card">
            <div className="card-icon">💡</div>

            <div>
              <div className="card-label">
                Why RECALL Recommends This
              </div>

              <div className="card-value">
                {why || "Insufficient historical evidence"}
              </div>
            </div>
          </div>


          <div className="analysis-card evidence-card">
            <div className="card-icon">📚</div>

            <div>
              <div className="card-label">
                Historical Evidence
              </div>

              <div className="card-value">
                {evidence || "No historical evidence found"}
              </div>
            </div>
          </div>

        </div>


        {/* Recovery */}

        <div className="recovery-card">

          <div className="recovery-icon">
            ⏱️
          </div>

          <div>
            <div className="card-label">
              Expected Recovery
            </div>

            <div className="recovery-value">
              {recovery || "Insufficient historical evidence"}
            </div>
          </div>

        </div>


        {/* Hindsight Memory Timeline */}

        <div className="memory-section">

          <div className="section-title">

            <div>
              <p className="eyebrow">
                LONG-TERM MEMORY
              </p>

              <h2>
                What RECALL Remembered
              </h2>
            </div>

            <span className="memory-count">
              {analysis.historical_memories?.length || 0} memories
            </span>

          </div>


          <div className="memory-timeline">

            {analysis.historical_memories?.map(
              (memory, index) => (

                <div
                  className="timeline-item"
                  key={index}
                >

                  <div className="timeline-marker">
                    <span>{index + 1}</span>
                  </div>

                  <div className="timeline-line"></div>

                  <div className="timeline-card">

                    <div className="timeline-header">

                      <span className="memory-tag">
                        HINDSIGHT MEMORY
                      </span>

                      <span className="memory-index">
                        #{index + 1}
                      </span>

                    </div>


                    <div className="timeline-content">
                      {memory}
                    </div>

                  </div>

                </div>

              )
            )}

          </div>

        </div>


        {/* Feedback */}

        <div className="feedback-card">

          <div>

            <p className="eyebrow">
              AFTER RESOLUTION
            </p>

            <h2>
              Did the recommendation work?
            </h2>

            <p className="feedback-description">
              Your feedback becomes part of RECALL's
              future memory.
            </p>

          </div>


          <div className="feedback-buttons">

            <button
              className="success-button"
              onClick={() =>
                sendFeedback("SUCCESSFUL")
              }
              disabled={feedbackLoading}
            >
              ✓ Resolution Worked
            </button>


            <button
              className="failure-button"
              onClick={() =>
                sendFeedback("FAILED")
              }
              disabled={feedbackLoading}
            >
              ✕ Didn't Work
            </button>

          </div>


          {feedbackMessage && (
            <p className="feedback-message">
              {feedbackMessage}
            </p>
          )}

        </div>

      </section>
    );
  };


  // -----------------------------
  // Main UI
  // -----------------------------

  return (
    <div className="app">

      {/* Header */}

      <header className="header">

        <div>
          <h1>RECALL</h1>
          <p>AI Incident Response Agent</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Operational
        </div>

      </header>


      {/* Main */}

      <main className="container">

        {/* Active Incident */}

        <section className="card">

          <div className="section-title">

            <div>
              <p className="eyebrow">
                ACTIVE INCIDENT
              </p>

              <h2>
                What's happening?
              </h2>
            </div>

            <span className="live-badge">
              LIVE
            </span>

          </div>


          <div className="form-grid">

            <div className="field">

              <label>
                Service
              </label>

              <input
                value={service}
                onChange={(e) =>
                  setService(e.target.value)
                }
              />

            </div>


            <div className="field">

              <label>
                Severity
              </label>

              <select
                value={severity}
                onChange={(e) =>
                  setSeverity(e.target.value)
                }
              >

                <option value="critical">
                  Critical
                </option>

                <option value="high">
                  High
                </option>

                <option value="medium">
                  Medium
                </option>

                <option value="low">
                  Low
                </option>

              </select>

            </div>

          </div>


          <div className="field">

            <label>
              Problem Description
            </label>

            <textarea
              value={problem}
              onChange={(e) =>
                setProblem(e.target.value)
              }
              rows="4"
            />

          </div>


          {/* Error Message */}

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}


          <button
            className="analyze-button"
            onClick={analyzeIncident}
            disabled={loading}
          >

            {loading
              ? "Analyzing..."
              : "Analyze Incident →"}

          </button>

        </section>


        {/* AI Analysis */}

        {renderAnalysis()}

      </main>

    </div>
  );
}

export default App;