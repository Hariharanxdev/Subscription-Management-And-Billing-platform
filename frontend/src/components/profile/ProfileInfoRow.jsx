export default function ProfileInfoRow({ label, value }) {
  return (
    <div className="leader-row text-sm">
      <span className="text-ink-faint">{label}</span>
      <span className="leader-fill" />
      <span className="tabular font-medium text-ink">{value ?? "—"}</span>
    </div>
  );
}
