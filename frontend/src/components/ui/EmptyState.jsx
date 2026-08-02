export default function EmptyState({ icon, title, description, action }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 px-6 text-center">
      {icon && (
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-ledger-50 text-ledger-500">
          {icon}
        </div>
      )}
      <div className="space-y-1">
        <p className="font-display text-lg text-ink">{title}</p>
        {description && <p className="text-sm text-ink-faint max-w-sm">{description}</p>}
      </div>
      {action}
    </div>
  );
}
