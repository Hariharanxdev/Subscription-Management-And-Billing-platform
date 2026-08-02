import { Link, Outlet } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { useAuth } from "../context/AuthContext";

export default function PublicLayout() {
  const { isAuthenticated, isAdmin } = useAuth();
  return (
    <div className="min-h-screen bg-paper">
      <header className="sticky top-0 z-30 border-b border-line bg-paper/85 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center gap-2.5 px-6 py-4">
          <Link to="/" className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-ledger-500">
              <svg width="16" height="16" viewBox="0 0 32 32" fill="none">
                <path d="M9 12h14M9 16h14M9 20h9" stroke="#F7F7F3" strokeWidth="2.4" strokeLinecap="round" />
              </svg>
            </div>
            <span className="font-display text-lg text-ink">Ledger</span>
          </Link>
          <nav className="ml-auto flex items-center gap-3">
            {isAuthenticated ? (
              <Link to={isAdmin ? "/admin/dashboard" : "/app/dashboard"} className="btn-primary">
                Go to dashboard
              </Link>
            ) : (
              <>
                <Link to="/login" className="btn-ghost">
                  Sign in
                </Link>
                <Link to="/register" className="btn-primary">
                  Get started
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-12">
        <Outlet />
      </main>
      <Toaster position="top-right" />
    </div>
  );
}
