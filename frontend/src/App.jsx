import { useEffect, useState } from "react";
import "./App.css";

const API = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

function money(n) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(n ?? 0);
}

export default function App() {
  const [summary, setSummary] = useState(null);
  const [payments, setPayments] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [s, p] = await Promise.all([
          fetch(`${API}/api/summary`).then((r) => r.json()),
          fetch(`${API}/api/payments?limit=100`).then((r) => r.json()),
        ]);
        setSummary(s);
        setPayments(p);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <p className="state">Loading…</p>;
  if (error) return <p className="state error">Could not reach the API: {error}</p>;

  return (
    <div className="page">
      <header>
        <h1>Stripe Payments</h1>
        <p className="sub">
          Last synced {summary.last_synced?.slice(0, 16).replace("T", " ")} UTC
        </p>
      </header>

      <section className="cards">
        <Card label="Gross volume" value={money(summary.gross)} />
        <Card label="Transactions" value={summary.transactions} />
        <Card label="Average payment" value={money(summary.average)} />
        <Card label="Records in database" value={summary.total_records} />
      </section>

      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Status</th>
            <th className="right">Amount</th>
          </tr>
        </thead>
        <tbody>
          {payments.map((p) => (
            <tr key={p.id}>
              <td>{p.created_at.slice(0, 16).replace("T", " ")}</td>
              <td>{p.description || "—"}</td>
              <td>
                <span className={`pill ${p.status}`}>{p.status}</span>
              </td>
              <td className="right">{money(p.amount)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Card({ label, value }) {
  return (
    <div className="card">
      <span className="label">{label}</span>
      <span className="value">{value}</span>
    </div>
  );
}