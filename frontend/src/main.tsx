import { StrictMode } from "react";
import type { FormEvent } from "react";
import { useState } from "react";
import { createRoot } from "react-dom/client";
import { AlertTriangle, Database, RefreshCw, Send } from "lucide-react";
import "./styles.css";

type DxBAResult = {
  batting_average: number;
  slugging: number;
  samples: number;
};

type DataOperationResult = {
  success: boolean;
  message: string;
  rows_affected: number;
};

type StatusKind = "idle" | "loading" | "success" | "error";

type Status = {
  kind: StatusKind;
  message: string;
};

async function postJson<TResponse>(url: string, body?: unknown): Promise<TResponse> {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<TResponse>;
}

function formatRate(value: number): string {
  return value.toFixed(3).replace(/^0/, "");
}

function App() {
  const [launchAngle, setLaunchAngle] = useNumericField("");
  const [exitVelocity, setExitVelocity] = useNumericField("");
  const [sprayAngle, setSprayAngle] = useNumericField("");
  const [angleForgiveness, setAngleForgiveness] = useNumericField("2");
  const [velocityForgiveness, setVelocityForgiveness] = useNumericField("2");
  const [launchForgiveness, setLaunchForgiveness] = useNumericField("2");
  const [result, setResult] = useState<DxBAResult | null>(null);
  const [calculatorStatus, setCalculatorStatus] = useState<Status>({
    kind: "idle",
    message: "",
  });
  const [adminStatus, setAdminStatus] = useState<Status>({ kind: "idle", message: "" });

  async function calculateDxBA(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCalculatorStatus({ kind: "loading", message: "Calculating..." });
    setResult(null);

    try {
      const response = await postJson<DxBAResult>("/api/dxba/calculate", {
        launch_angle: Number(launchAngle),
        exit_velocity: Number(exitVelocity),
        spray_angle: Number(sprayAngle),
        angle_forgiveness: Number(angleForgiveness),
        velocity_forgiveness: Number(velocityForgiveness),
        launch_forgiveness: Number(launchForgiveness),
      });

      setResult(response);
      setCalculatorStatus({ kind: "success", message: "Calculation complete." });
    } catch (error) {
      setCalculatorStatus({
        kind: "error",
        message: error instanceof Error ? error.message : "Calculation failed.",
      });
    }
  }

  async function resetData() {
    const confirmed = window.confirm(
      "Resetting data will drop and recreate the DxBA table. Continue?"
    );

    if (!confirmed) {
      return;
    }

    await runAdminOperation("/api/data/reset", "Resetting data...");
  }

  async function importData() {
    await runAdminOperation("/api/data/import", "Importing Statcast data...");
  }

  async function runAdminOperation(url: string, loadingMessage: string) {
    setAdminStatus({ kind: "loading", message: loadingMessage });

    try {
      const response = await postJson<DataOperationResult>(url);
      setAdminStatus({
        kind: response.success ? "success" : "error",
        message: `${response.message} Rows affected: ${response.rows_affected}.`,
      });
    } catch (error) {
      setAdminStatus({
        kind: "error",
        message: error instanceof Error ? error.message : "Data operation failed.",
      });
    }
  }

  const calculatorBusy = calculatorStatus.kind === "loading";
  const adminBusy = adminStatus.kind === "loading";

  return (
    <main className="app-shell">
      <section className="workspace">
        <header className="app-header">
          <div>
            <p className="eyebrow">BatMath</p>
            <h1>Adjusted batted-ball outcomes</h1>
          </div>
          <div className="status-pill">Local API</div>
        </header>

        <div className="layout-grid">
          <form className="calculator-panel" onSubmit={calculateDxBA}>
            <div className="panel-heading">
              <h2>DxBA Calculator</h2>
              <button type="submit" className="primary-button" disabled={calculatorBusy}>
                {calculatorBusy ? <RefreshCw className="spin" size={18} /> : <Send size={18} />}
                Calculate
              </button>
            </div>

            <div className="input-grid">
              <NumberInput
                label="Launch angle"
                value={launchAngle}
                onChange={setLaunchAngle}
                required
              />
              <NumberInput
                label="Exit velocity"
                value={exitVelocity}
                onChange={setExitVelocity}
                required
              />
              <NumberInput
                label="Spray angle"
                value={sprayAngle}
                onChange={setSprayAngle}
                required
              />
            </div>

            <div className="secondary-controls">
              <h3>Forgiveness</h3>
              <div className="input-grid compact">
                <NumberInput
                  label="Angle"
                  value={angleForgiveness}
                  onChange={setAngleForgiveness}
                  required
                />
                <NumberInput
                  label="Velocity"
                  value={velocityForgiveness}
                  onChange={setVelocityForgiveness}
                  required
                />
                <NumberInput
                  label="Launch"
                  value={launchForgiveness}
                  onChange={setLaunchForgiveness}
                  required
                />
              </div>
            </div>

            <StatusMessage status={calculatorStatus} />
          </form>

          <aside className="results-panel">
            <h2>Result</h2>
            {result === null ? (
              <div className="empty-state">Run a calculation to see adjusted outcomes.</div>
            ) : (
              <div className="metric-grid">
                <Metric label="Average" value={formatRate(result.batting_average)} />
                <Metric label="Slugging" value={formatRate(result.slugging)} />
                <Metric label="Samples" value={result.samples.toLocaleString()} />
              </div>
            )}
          </aside>
        </div>

        <section className="admin-panel">
          <div>
            <p className="eyebrow">Admin</p>
            <h2>Data operations</h2>
          </div>
          <div className="admin-actions">
            <button type="button" className="secondary-button danger" onClick={resetData} disabled={adminBusy}>
              <AlertTriangle size={18} />
              Reset Data
            </button>
            <button type="button" className="secondary-button" onClick={importData} disabled={adminBusy}>
              {adminBusy ? <RefreshCw className="spin" size={18} /> : <Database size={18} />}
              Import Statcast
            </button>
          </div>
          <StatusMessage status={adminStatus} />
        </section>
      </section>
    </main>
  );
}

function useNumericField(initialValue: string) {
  return useState(initialValue);
}

type NumberInputProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
};

function NumberInput({ label, value, onChange, required = false }: NumberInputProps) {
  return (
    <label className="field">
      <span>{label}</span>
      <input
        type="number"
        step="any"
        value={value}
        required={required}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function StatusMessage({ status }: { status: Status }) {
  if (status.kind === "idle" || status.message === "") {
    return null;
  }

  return <div className={`status-message ${status.kind}`}>{status.message}</div>;
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
