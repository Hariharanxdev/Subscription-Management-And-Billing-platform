import { useCountUp } from "../../hooks/useCountUp";
import { formatCurrency } from "../../utils/format";

export default function StatCard({ label, value, icon, format = "number", accent = false }) {
  const animated = useCountUp(value);

  const display =
    format === "currency"
      ? formatCurrency(animated)
      : Math.round(animated).toLocaleString("en-IN");

  return (
    <div className={`card p-5 ${accent ? "border-ledger-500/40" : ""}`}>
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wider text-ink-faint">{label}</p>
        {icon && <span className="text-ledger-500">{icon}</span>}
      </div>
      <p className="mt-2.5 text-2xl font-semibold tabular text-ink">{display}</p>
    </div>
  );
}
