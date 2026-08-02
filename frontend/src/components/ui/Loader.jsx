export function Spinner({ size = 20, className = "" }) {
  return (
    <span
      className={`inline-block rounded-full border-2 border-ledger-200 border-t-ledger-500 animate-spin ${className}`}
      style={{ width: size, height: size }}
    />
  );
}

export function PageLoader({ label = "Loading" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-24 text-ink-faint">
      <Spinner size={28} />
      <p className="text-sm tabular tracking-wide">{label}…</p>
    </div>
  );
}

export function Skeleton({ className = "" }) {
  return <div className={`animate-pulse rounded-md bg-ink/[0.06] ${className}`} />;
}

export function SkeletonRow() {
  return (
    <div className="flex items-center gap-4 py-4">
      <Skeleton className="h-4 w-1/4" />
      <Skeleton className="h-4 w-1/6" />
      <Skeleton className="h-4 w-1/6" />
      <Skeleton className="h-4 w-1/6 ml-auto" />
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="card p-6 space-y-3">
      <Skeleton className="h-3 w-1/3" />
      <Skeleton className="h-7 w-1/2" />
      <Skeleton className="h-3 w-2/3" />
    </div>
  );
}
