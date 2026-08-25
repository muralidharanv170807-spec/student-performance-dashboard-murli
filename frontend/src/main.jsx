import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const DEFAULT_FORM = {
  attendance: 85,
  internal_marks: 78,
  assignment_percentage: 90,
  study_hours: 4,
  previous_marks: 82,
};

const fieldLabels = {
  attendance: "Attendance",
  internal_marks: "Internal Marks",
  assignment_percentage: "Assignments",
  study_hours: "Study Hours",
  previous_marks: "Previous Marks",
};

function App() {
  const [formData, setFormData] = useState(DEFAULT_FORM);
  const [whatIfData, setWhatIfData] = useState(DEFAULT_FORM);
  const [result, setResult] = useState(null);
  const [whatIfResult, setWhatIfResult] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [history, setHistory] = useState([]);
  const [featureImportance, setFeatureImportance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [whatIfLoading, setWhatIfLoading] = useState(false);
  const [error, setError] = useState("");

  const maxImportance = useMemo(
    () => Math.max(...(featureImportance.map((item) => item.importance) || [1]), 1),
    [featureImportance]
  );

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((current) => ({
      ...current,
      [name]: value === "" ? "" : Number(value),
    }));
  };

  const handleWhatIfChange = (e) => {
    const { name, value } = e.target;
    setWhatIfData((current) => ({
      ...current,
      [name]: value === "" ? "" : Number(value),
    }));
  };

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`${API_BASE}/analytics`);
      if (!response.ok) throw new Error("Analytics unavailable");
      const data = await response.json();
      setAnalytics(data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_BASE}/prediction-history`);
      if (!response.ok) throw new Error("History unavailable");
      const data = await response.json();
      setHistory(data.history || []);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchFeatureImportance = async () => {
    try {
      const response = await fetch(`${API_BASE}/feature-importance`);
      if (!response.ok) throw new Error("Feature importance unavailable");
      const data = await response.json();
      setFeatureImportance(data.feature_importance || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          attendance: Number(formData.attendance),
          internal_marks: Number(formData.internal_marks),
          assignment_percentage: Number(formData.assignment_percentage),
          study_hours: Number(formData.study_hours),
          previous_marks: Number(formData.previous_marks),
        }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail ? payload.detail[0]?.msg || "Invalid input" : "Prediction failed");
      }

      const data = await response.json();
      setResult(data);
      await fetchAnalytics();
      await fetchHistory();
    } catch (err) {
      setError(err.message || "Unable to connect to the prediction server.");
    } finally {
      setLoading(false);
    }
  };

  const handleWhatIf = async () => {
    setWhatIfLoading(true);
    setWhatIfResult(null);

    try {
      const response = await fetch(`${API_BASE}/what-if`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current: {
            attendance: Number(formData.attendance),
            internal_marks: Number(formData.internal_marks),
            assignment_percentage: Number(formData.assignment_percentage),
            study_hours: Number(formData.study_hours),
            previous_marks: Number(formData.previous_marks),
          },
          modified: {
            attendance: Number(whatIfData.attendance),
            internal_marks: Number(whatIfData.internal_marks),
            assignment_percentage: Number(whatIfData.assignment_percentage),
            study_hours: Number(whatIfData.study_hours),
            previous_marks: Number(whatIfData.previous_marks),
          },
        }),
      });

      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail ? payload.detail[0]?.msg || "What-if analysis failed" : "What-if analysis failed");
      }

      const data = await response.json();
      setWhatIfResult(data);
    } catch (err) {
      setError(err.message || "Unable to compare predictions.");
    } finally {
      setWhatIfLoading(false);
    }
  };

  const downloadReport = () => {
    if (!result) return;

    const content = [
      "Student Performance Report",
      "========================",
      `Prediction: ${result.prediction}`,
      `Confidence: ${result.confidence}%`,
      `Risk Level: ${result.risk_level}`,
      "",
      "Input Features:",
      ...Object.entries(formData).map(([key, value]) => `${fieldLabels[key]}: ${value}`),
      "",
      "Recommendations:",
      ...(result.recommendations || []).map((item) => `- ${item}`),
      "",
      "Reasons:",
      ...(result.reasons || []).map((item) => `- ${item}`),
    ].join("\n");

    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `student-report-${result.prediction.toLowerCase()}.txt`;
    anchor.click();
    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    fetchAnalytics();
    fetchHistory();
    fetchFeatureImportance();
  }, []);

  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI + STUDENT SUCCESS</p>
          <h1>Student Performance Dashboard</h1>
        </div>
      </header>

      <main className="main-grid">
        <section className="panel form-panel">
          <h2>Student Input</h2>
          <form onSubmit={handleSubmit} className="form-grid">
            {Object.entries(fieldLabels).map(([key, label]) => (
              <label className="field" key={key}>
                <span>{label}</span>
                <input
                  type="number"
                  name={key}
                  min={key === "study_hours" ? 0 : 0}
                  max={key === "study_hours" ? 24 : 100}
                  step={key === "study_hours" ? "0.1" : "1"}
                  value={formData[key]}
                  onChange={handleChange}
                  required
                />
              </label>
            ))}

            <div className="button-row">
              <button type="submit" disabled={loading}>
                {loading ? "Predicting..." : "Predict Performance"}
              </button>
              <button type="button" className="secondary" onClick={() => setFormData(DEFAULT_FORM)}>
                Reset
              </button>
            </div>
          </form>

          {error && <div className="error-box">{error}</div>}

          {result && (
            <div className="result-panel">
              <div className="result-header">
                <div>
                  <p className="label">Performance</p>
                  <h3>{result.prediction}</h3>
                </div>
                <div className="badge danger">{result.risk_level} Risk</div>
              </div>

              <div className="stats-grid">
                <div className="stat-card">
                  <span>Confidence</span>
                  <strong>{result.confidence}%</strong>
                </div>
                <div className="stat-card">
                  <span>Attendance</span>
                  <strong>{formData.attendance}%</strong>
                </div>
                <div className="stat-card">
                  <span>Internal</span>
                  <strong>{formData.internal_marks}%</strong>
                </div>
                <div className="stat-card">
                  <span>Assignments</span>
                  <strong>{formData.assignment_percentage}%</strong>
                </div>
                <div className="stat-card">
                  <span>Study Hours</span>
                  <strong>{formData.study_hours}h</strong>
                </div>
                <div className="stat-card">
                  <span>Previous Marks</span>
                  <strong>{formData.previous_marks}%</strong>
                </div>
              </div>

              <div className="recommendations-box">
                <h4>Personalized Recommendations</h4>
                <ul>
                  {(result.recommendations || []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="recommendations-box">
                <h4>Risk Reasons</h4>
                <ul>
                  {(result.reasons || []).length ? (
                    (result.reasons || []).map((item) => <li key={item}>{item}</li>)
                  ) : (
                    <li>No risk indicators were identified for this profile.</li>
                  )}
                </ul>
              </div>

              <button type="button" className="secondary report-button" onClick={downloadReport}>
                Download Report
              </button>
            </div>
          )}
        </section>

        <aside className="panel analytics-panel">
          <h2>Analytics Snapshot</h2>
          {analytics ? (
            <div className="mini-grid">
              <div className="mini-card">
                <span>Total Predictions</span>
                <strong>{analytics.total_predictions}</strong>
              </div>
              <div className="mini-card">
                <span>Good</span>
                <strong>{analytics.good_predictions}</strong>
              </div>
              <div className="mini-card">
                <span>Average</span>
                <strong>{analytics.average_predictions}</strong>
              </div>
              <div className="mini-card">
                <span>Poor</span>
                <strong>{analytics.poor_predictions}</strong>
              </div>
              <div className="mini-card">
                <span>At-Risk</span>
                <strong>{analytics.at_risk_students}</strong>
              </div>
              <div className="mini-card">
                <span>Avg Attendance</span>
                <strong>{analytics.average_attendance}%</strong>
              </div>
              <div className="mini-card">
                <span>Avg Marks</span>
                <strong>{analytics.average_marks}%</strong>
              </div>
              <div className="mini-card">
                <span>Avg Study Hrs</span>
                <strong>{analytics.average_study_hours}h</strong>
              </div>
            </div>
          ) : (
            <p>Loading analytics...</p>
          )}

          <div className="feature-panel">
            <h3>Feature Importance</h3>
            {featureImportance.length ? (
              featureImportance.map((item) => (
                <div className="bar-row" key={item.feature}>
                  <div className="bar-labels">
                    <span>{item.label}</span>
                    <span>{item.importance}</span>
                  </div>
                  <div className="bar-track">
                    <div
                      className="bar-fill"
                      style={{ width: `${(item.importance / maxImportance) * 100}%` }}
                    />
                  </div>
                </div>
              ))
            ) : (
              <p>Loading model feature importance...</p>
            )}
          </div>
        </aside>
      </main>

      <section className="panel whatif-panel">
        <h2>What-If Analysis</h2>
        <div className="whatif-grid">
          <div>
            <h3>Current Inputs</h3>
            <div className="compare-grid">
              {Object.entries(fieldLabels).map(([key, label]) => (
                <label className="field" key={`current-${key}`}>
                  <span>{label}</span>
                  <input
                    type="number"
                    value={formData[key]}
                    onChange={handleChange}
                    name={key}
                    min={0}
                    max={key === "study_hours" ? 24 : 100}
                    step={key === "study_hours" ? "0.1" : "1"}
                  />
                </label>
              ))}
            </div>
          </div>

          <div>
            <h3>Modified Inputs</h3>
            <div className="compare-grid">
              {Object.entries(fieldLabels).map(([key, label]) => (
                <label className="field" key={`modified-${key}`}>
                  <span>{label}</span>
                  <input
                    type="number"
                    value={whatIfData[key]}
                    onChange={handleWhatIfChange}
                    name={key}
                    min={0}
                    max={key === "study_hours" ? 24 : 100}
                    step={key === "study_hours" ? "0.1" : "1"}
                  />
                </label>
              ))}
            </div>
          </div>
        </div>

        <button type="button" className="what-if-button" onClick={handleWhatIf} disabled={whatIfLoading}>
          {whatIfLoading ? "Comparing..." : "Run What-If Analysis"}
        </button>

        {whatIfResult && (
          <div className="comparison-box">
            <div className="comparison-row">
              <div>
                <p className="label">Current Prediction</p>
                <h3>{whatIfResult.current.prediction}</h3>
              </div>
              <div>
                <p className="label">Modified Prediction</p>
                <h3>{whatIfResult.modified.prediction}</h3>
              </div>
            </div>
            <p className="change-text">Prediction: {whatIfResult.difference}</p>
          </div>
        )}
      </section>

      <section className="panel history-panel">
        <h2>Prediction History</h2>
        {history.length ? (
          <div className="history-list">
            {history.slice(0, 6).map((record) => (
              <div key={record.id} className="history-item">
                <div>
                  <strong>{record.prediction}</strong>
                  <span>{new Date(record.created_at).toLocaleString()}</span>
                </div>
                <div className="history-meta">
                  <span>{record.confidence}%</span>
                  <span>{record.risk_level}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No predictions recorded yet.</p>
        )}
      </section>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);