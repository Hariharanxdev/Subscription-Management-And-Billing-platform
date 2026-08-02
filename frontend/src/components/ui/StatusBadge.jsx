const MAP = {
  active: { cls: "badge-active", dot: "bg-ledger-500" },
  success: { cls: "badge-success", dot: "bg-ledger-500" },
  paid: { cls: "badge-success", dot: "bg-ledger-500" },
  cancelled: { cls: "badge-cancelled", dot: "bg-ink-faint" },
  expired: { cls: "badge-expired", dot: "bg-brick-500" },
  failed: { cls: "badge-expired", dot: "bg-brick-500" },
  pending: { cls: "badge-pending", dot: "bg-gold-500" },
};

export default function StatusBadge({ status }) {
  const key = (status || "").toLowerCase();
  const config = MAP[key] || MAP.pending;
  return (
    <span className={config.cls}>
      <span className={`h-1.5 w-1.5 rounded-full ${config.dot}`} />
      {status}
    </span>
  );
}
