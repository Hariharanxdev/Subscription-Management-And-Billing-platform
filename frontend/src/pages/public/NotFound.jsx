import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-3 bg-paper px-6 text-center">
      <p className="font-display text-6xl text-ledger-500 tabular">404</p>
      <h1 className="font-display text-xl text-ink">This page isn't in the ledger.</h1>
      <p className="text-sm text-ink-faint max-w-sm">
        The page you're looking for doesn't exist or may have moved.
      </p>
      <Link to="/" className="btn-primary mt-3">
        Back to home
      </Link>
    </div>
  );
}
