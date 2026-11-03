
"use client";

import { useEffect, useMemo, useState } from "react";

type ChargebackCase = {
  case_id: string;
  transaction_id: string;
  transaction_date: string;
  amount: number;
  dispute_reason: string;
  current_stage: string;
  representment_status: string;
  final_outcome: string;
  loss_amount: number;
};

const STAGES = [
  "Purchase",
  "Dispute Filed",
  "Chargeback",
  "Merchant Response",
  "Representment",
  "Final Decision",
];

const API_URL =
  "https://poc6-chargeback-backend.onrender.com";

const money = (amount: number) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);

function outcomeClass(outcome: string) {
  if (outcome === "Won") return "status-won";
  if (outcome === "Lost") return "status-lost";
  return "status-pending";
}

export default function Home() {
  const [cases, setCases] = useState<ChargebackCase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [reasonFilter, setReasonFilter] = useState("All");
  const [stageFilter, setStageFilter] = useState("All");
  const [outcomeFilter, setOutcomeFilter] = useState("All");

  const [selectedCase, setSelectedCase] =
    useState<ChargebackCase | null>(null);
  const [metadataOpen, setMetadataOpen] = useState(false);

  useEffect(() => {
    let active = true;

    async function loadData() {
      try {
        const response = await fetch(
          `${API_URL}/api/chargebacks`
        );

        if (!response.ok) {
          throw new Error(
            `Failed to fetch chargeback cases: ${response.status}`
          );
        }

        const data: ChargebackCase[] = await response.json();

        if (active) {
          setCases(data);
          setError(null);
        }
      } catch (err) {
        console.error("Failed to load chargeback data:", err);

        if (active) {
          setError(
            "Unable to load chargeback intelligence. Please make sure the FastAPI backend is running and try again."
          );
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    loadData();

    return () => {
      active = false;
    };
  }, []);

  const filteredCases = useMemo(
    () =>
      cases.filter((item) => {
        const matchesReason =
          reasonFilter === "All" ||
          item.dispute_reason === reasonFilter;

        const matchesStage =
          stageFilter === "All" ||
          item.current_stage === stageFilter;

        const matchesOutcome =
          outcomeFilter === "All" ||
          item.final_outcome === outcomeFilter;

        return matchesReason && matchesStage && matchesOutcome;
      }),
    [cases, reasonFilter, stageFilter, outcomeFilter]
  );

  const summary = useMemo(() => {
    return {
      total: filteredCases.length,
      amount: filteredCases.reduce(
        (sum, item) => sum + item.amount,
        0
      ),
      loss: filteredCases.reduce(
        (sum, item) => sum + item.loss_amount,
        0
      ),
      pending: filteredCases.filter(
        (item) => item.final_outcome === "Pending"
      ).length,
      won: filteredCases.filter(
        (item) => item.final_outcome === "Won"
      ).length,
      lost: filteredCases.filter(
        (item) => item.final_outcome === "Lost"
      ).length,
    };
  }, [filteredCases]);

  const stageCounts = useMemo(() => {
    const counts: Record<string, number> = {};

    filteredCases.forEach((item) => {
      counts[item.current_stage] =
        (counts[item.current_stage] || 0) + 1;
    });

    return counts;
  }, [filteredCases]);

  const reasonCounts = useMemo(() => {
    const counts: Record<string, number> = {};

    filteredCases.forEach((item) => {
      counts[item.dispute_reason] =
        (counts[item.dispute_reason] || 0) + 1;
    });

    return counts;
  }, [filteredCases]);

  function downloadSampleData() {
    const blob = new Blob(
      [JSON.stringify(cases, null, 2)],
      { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "chargeback_sample_data.json";
    link.click();

    URL.revokeObjectURL(url);
  }

  function resetFilters() {
    setReasonFilter("All");
    setStageFilter("All");
    setOutcomeFilter("All");
  }

  if (loading) {
    return (
      <main className="loading-screen">
        <div className="loading-orbit" />
        <p>Initializing chargeback intelligence</p>
        <span>CONNECTING TO CASE DATA</span>
      </main>
    );
  }

  if (error) {
    return (
      <main className="loading-screen">
        <div className="error-card">
          <span className="eyebrow">SYSTEM CONNECTION</span>
          <h1>Intelligence unavailable</h1>
          <p>{error}</p>
          <button
            className="primary-button"
            onClick={() => window.location.reload()}
          >
            Retry connection
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="command-center">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark">C</div>
          <div>
            <p className="brand-name">CHARGEBACK</p>
            <p className="brand-subtitle">
              LIFECYCLE INTELLIGENCE
            </p>
          </div>
        </div>

        <div className="topbar-right">
          <div className="live-indicator">
            <span />
            DATA CONNECTED
          </div>

          <button
            className="metadata-trigger"
            onClick={() => setMetadataOpen(true)}
            aria-label="Open project information"
          >
            <span className="metadata-avatar">JP</span>
            <span className="metadata-label">PROJECT INFO</span>
            <span className="metadata-chevron">↗</span>
          </button>
        </div>
      </header>

      <div className="page-content">
        <section className="hero-section">
          <div>
            <p className="eyebrow">
              <span className="eyebrow-line" />
              PAYMENT OPERATIONS / DISPUTE ANALYTICS
            </p>

            <h1>
              Chargeback
              <br />
              <span>Lifecycle.</span>
            </h1>

            <p className="hero-description">
              A unified view of payment disputes, representment
              progress and financial outcomes across the
              chargeback lifecycle.
            </p>
          </div>

          <div className="hero-index">
            <span>OPERATIONAL OVERVIEW</span>
            <strong>06</strong>
            <span>CASE INTELLIGENCE</span>
          </div>
        </section>

        <section className="metrics-grid">
          <article className="metric-card metric-primary">
            <div className="metric-heading">
              <span>TOTAL CASES</span>
              <span className="metric-icon">◎</span>
            </div>
            <strong>{summary.total}</strong>
            <p>Cases in current view</p>
          </article>

          <article className="metric-card">
            <div className="metric-heading">
              <span>TRANSACTION VALUE</span>
              <span className="metric-icon">↗</span>
            </div>
            <strong>{money(summary.amount)}</strong>
            <p>Disputed transaction volume</p>
          </article>

          <article className="metric-card">
            <div className="metric-heading">
              <span>TOTAL LOSS</span>
              <span className="metric-icon loss-icon">↘</span>
            </div>
            <strong className="loss-value">
              {money(summary.loss)}
            </strong>
            <p>Recorded financial exposure</p>
          </article>

          <article className="metric-card">
            <div className="metric-heading">
              <span>PENDING CASES</span>
              <span className="metric-icon pending-icon">◷</span>
            </div>
            <strong>{summary.pending}</strong>
            <p>Awaiting final outcome</p>
          </article>
        </section>

        <section className="section-block">
          <div className="section-heading">
            <div>
              <p className="eyebrow">01 / PROCESS VISIBILITY</p>
              <h2>Lifecycle overview</h2>
              <p className="section-description">
                Distribution of cases across the dispute journey.
              </p>
            </div>
            <span className="section-count">
              {filteredCases.length} RECORDS
            </span>
          </div>

          <div className="lifecycle-track">
            {STAGES.map((stage, index) => {
              const count = stageCounts[stage] || 0;
              const percentage =
                filteredCases.length > 0
                  ? (count / filteredCases.length) * 100
                  : 0;

              return (
                <div className="stage-item" key={stage}>
                  <div className="stage-topline">
                    <span className="stage-number">
                      0{index + 1}
                    </span>
                    <span className="stage-count">{count}</span>
                  </div>

                  <div className="stage-track">
                    <div
                      className="stage-fill"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>

                  <p>{stage}</p>
                </div>
              );
            })}
          </div>
        </section>

        <section className="section-block">
          <div className="section-heading">
            <div>
              <p className="eyebrow">02 / DISPUTE CLASSIFICATION</p>
              <h2>Reason distribution</h2>
              <p className="section-description">
                Breakdown by recorded dispute category.
              </p>
            </div>
          </div>

          <div className="distribution-grid">
            {Object.entries(reasonCounts).map(
              ([reason, count], index) => {
                const percentage =
                  filteredCases.length > 0
                    ? (count / filteredCases.length) * 100
                    : 0;

                return (
                  <article
                    className="distribution-card"
                    key={reason}
                  >
                    <div className="distribution-top">
                      <span className="distribution-index">
                        0{index + 1}
                      </span>
                      <span>{percentage.toFixed(1)}%</span>
                    </div>

                    <h3>{reason}</h3>

                    <div className="distribution-track">
                      <div
                        className="distribution-fill"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>

                    <p>
                      {count} {count === 1 ? "case" : "cases"}
                    </p>
                  </article>
                );
              }
            )}

            {filteredCases.length === 0 && (
              <p className="empty-message">
                No cases match the selected filters.
              </p>
            )}
          </div>
        </section>

        <section className="section-block cases-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">03 / CASE REGISTER</p>
              <h2>Dispute intelligence</h2>
              <p className="section-description">
                Select a case to inspect its lifecycle details.
              </p>
            </div>

            <button
              className="download-button"
              onClick={downloadSampleData}
            >
              ↓ EXPORT DATA
            </button>
          </div>

          <div className="filter-bar">
            <label>
              <span>REASON</span>
              <select
                value={reasonFilter}
                onChange={(e) => setReasonFilter(e.target.value)}
              >
                <option value="All">All reasons</option>
                <option value="Fraudulent transaction">
                  Fraudulent transaction
                </option>
                <option value="Product not received">
                  Product not received
                </option>
                <option value="Duplicate charge">
                  Duplicate charge
                </option>
              </select>
            </label>

            <label>
              <span>STAGE</span>
              <select
                value={stageFilter}
                onChange={(e) => setStageFilter(e.target.value)}
              >
                <option value="All">All stages</option>
                {STAGES.filter(
                  (stage) => stage !== "Purchase"
                ).map((stage) => (
                  <option key={stage} value={stage}>
                    {stage}
                  </option>
                ))}
              </select>
            </label>

            <label>
              <span>OUTCOME</span>
              <select
                value={outcomeFilter}
                onChange={(e) => setOutcomeFilter(e.target.value)}
              >
                <option value="All">All outcomes</option>
                <option value="Won">Won</option>
                <option value="Lost">Lost</option>
                <option value="Pending">Pending</option>
              </select>
            </label>

            <button
              className="reset-button"
              onClick={resetFilters}
            >
              RESET ↺
            </button>
          </div>

          <div className="table-wrap">
            <table className="case-table">
              <thead>
                <tr>
                  <th>CASE / TRANSACTION</th>
                  <th>AMOUNT</th>
                  <th>DISPUTE REASON</th>
                  <th>CURRENT STAGE</th>
                  <th>OUTCOME</th>
                  <th />
                </tr>
              </thead>

              <tbody>
                {filteredCases.map((item) => (
                  <tr
                    key={item.case_id}
                    className={
                      selectedCase?.case_id === item.case_id
                        ? "selected-row"
                        : ""
                    }
                    onClick={() => setSelectedCase(item)}
                  >
                    <td>
                      <strong>{item.case_id}</strong>
                      <span className="table-subtext">
                        {item.transaction_id}
                      </span>
                    </td>

                    <td className="amount-cell">
                      {money(item.amount)}
                    </td>

                    <td>{item.dispute_reason}</td>

                    <td>
                      <span className="stage-tag">
                        {item.current_stage}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`outcome-tag ${outcomeClass(
                          item.final_outcome
                        )}`}
                      >
                        {item.final_outcome}
                      </span>
                    </td>

                    <td className="row-arrow">↗</td>
                  </tr>
                ))}

                {filteredCases.length === 0 && (
                  <tr>
                    <td colSpan={6} className="empty-table">
                      No cases match the selected filters.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <div className="table-footer">
            <span>
              DISPLAYING {filteredCases.length} OF {cases.length} CASES
            </span>
            <span>SYNTHETIC DATASET / POC-6</span>
          </div>
        </section>

        <section className="outcomes-strip">
          <div>
            <p className="eyebrow">04 / OUTCOME SUMMARY</p>
            <h2>Resolution intelligence</h2>
          </div>

          <div className="outcome-summary">
            <div>
              <span className="outcome-dot won-dot" />
              <strong>{summary.won}</strong>
              <span>WON</span>
            </div>
            <div>
              <span className="outcome-dot lost-dot" />
              <strong>{summary.lost}</strong>
              <span>LOST</span>
            </div>
            <div>
              <span className="outcome-dot pending-dot" />
              <strong>{summary.pending}</strong>
              <span>PENDING</span>
            </div>
          </div>
        </section>

        <footer className="page-footer">
          <span>INFOCREON INTERNSHIP</span>
          <span>CHARGEBACK LIFECYCLE INTELLIGENCE</span>
          <span>POC-6 / 2026</span>
        </footer>
      </div>

      {selectedCase && (
        <>
          <button
            className="panel-backdrop"
            aria-label="Close case details"
            onClick={() => setSelectedCase(null)}
          />

          <aside
            className="insight-panel"
            aria-label="Selected chargeback case details"
          >
            <div className="panel-header">
              <div>
                <p className="eyebrow">CASE INTELLIGENCE</p>
                <h2>{selectedCase.case_id}</h2>
              </div>

              <button
                className="panel-close"
                onClick={() => setSelectedCase(null)}
                aria-label="Close panel"
              >
                ×
              </button>
            </div>

            <div className="panel-status">
              <span
                className={`outcome-tag ${outcomeClass(
                  selectedCase.final_outcome
                )}`}
              >
                {selectedCase.final_outcome}
              </span>
              <span>{selectedCase.current_stage}</span>
            </div>

            <div className="panel-amount">
              <span>DISPUTED AMOUNT</span>
              <strong>{money(selectedCase.amount)}</strong>
              <p>
                Recorded loss: {money(selectedCase.loss_amount)}
              </p>
            </div>

            <div className="panel-divider" />

            <p className="eyebrow">TRANSACTION DETAILS</p>

            <div className="detail-list">
              <div>
                <span>Case reference</span>
                <strong>{selectedCase.case_id}</strong>
              </div>
              <div>
                <span>Transaction ID</span>
                <strong>{selectedCase.transaction_id}</strong>
              </div>
              <div>
                <span>Transaction date</span>
                <strong>{selectedCase.transaction_date}</strong>
              </div>
              <div>
                <span>Dispute reason</span>
                <strong>{selectedCase.dispute_reason}</strong>
              </div>
              <div>
                <span>Representment</span>
                <strong>{selectedCase.representment_status}</strong>
              </div>
              <div>
                <span>Final outcome</span>
                <strong>{selectedCase.final_outcome}</strong>
              </div>
            </div>

            <div className="panel-note">
              <p className="eyebrow">LIFECYCLE POSITION</p>
              <p>
                This case is currently recorded at{" "}
                <strong>{selectedCase.current_stage}</strong>.
                Its representment status is{" "}
                <strong>{selectedCase.representment_status}</strong>.
              </p>
            </div>

            <p className="panel-footnote">
              CASE DATA / SYNTHETIC PROOF OF CONCEPT
            </p>
          </aside>
        </>
      )}

      {metadataOpen && (
        <div
          className="modal-backdrop"
          onClick={() => setMetadataOpen(false)}
        >
          <section
            className="metadata-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="metadata-title"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-topline">
              <span className="eyebrow">PROJECT CREDENTIALS</span>
              <button
                className="panel-close"
                onClick={() => setMetadataOpen(false)}
                aria-label="Close project information"
              >
                ×
              </button>
            </div>

            <div className="modal-emblem">C</div>

            <p className="eyebrow">INFOCREON INTERNSHIP</p>
            <h2 id="metadata-title">
              Chargeback
              <br />
              Lifecycle.
            </h2>

            <div className="metadata-details">
              <div>
                <span>ARCHITECT</span>
                <strong>Jona Peter</strong>
              </div>

              <div>
                <span>BATCH</span>
                <strong>Batch 8 Interns</strong>
              </div>

              <div>
                <span>STACK</span>
                <strong>
                  Next.js, FastAPI, Tailwind CSS, CSS-based data visualizations
                </strong>
              </div>

              <div>
                <span>PROJECT IDENTIFIER</span>
                <strong>PoC-6</strong>
              </div>

              <div>
                <span>GITHUB</span>
                <strong>@jonahpeter2006-12</strong>
              </div>

              <div>
                <span>PROGRAM</span>
                <strong>Infocreon Internship</strong>
              </div>
            </div>

            <p className="modal-footer">
              PAYMENT DISPUTE INTELLIGENCE / 2026
            </p>
          </section>
        </div>
      )}
    </main>
  );
}
