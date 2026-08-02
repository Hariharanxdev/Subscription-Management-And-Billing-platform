import { Outlet, Link } from "react-router-dom";
import { Toaster } from "react-hot-toast";

export default function AuthLayout() {
  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-paper">
      {/* Brand panel */}
      <div className="relative hidden lg:flex flex-col justify-between overflow-hidden bg-ledger-900 px-12 py-10 text-paper">
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.07]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(247,247,243,1) 1px, transparent 1px), linear-gradient(90deg, rgba(247,247,243,1) 1px, transparent 1px)",
            backgroundSize: "42px 42px",
          }}
        />
        <div
          className="pointer-events-none absolute -right-32 -top-32 h-96 w-96 rounded-full opacity-30 blur-3xl"
          style={{ background: "radial-gradient(circle, #C9A227 0%, transparent 70%)" }}
        />

        <Link to="/" className="relative flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-paper/10 border border-paper/20">
            <svg width="16" height="16" viewBox="0 0 32 32" fill="none">
              <path d="M9 12h14M9 16h14M9 20h9" stroke="#F7F7F3" strokeWidth="2.4" strokeLinecap="round" />
            </svg>
          </div>
          <span className="font-display text-lg">Ledger</span>
        </Link>

        <div className="relative space-y-6">
          <p className="font-display text-[2.75rem] leading-[1.08] max-w-md">
            Every subscription,
            <br />
            <em className="text-gold-300 not-italic font-medium">accounted for.</em>
          </p>
          <div className="max-w-sm space-y-3 text-sm text-paper/70 tabular">
            <div className="leader-row">
              <span>Active subscriptions</span>
              <span className="leader-fill !border-paper/20" />
              <span className="text-paper">tracked</span>
            </div>
            <div className="leader-row">
              <span>Invoices generated</span>
              <span className="leader-fill !border-paper/20" />
              <span className="text-paper">automatically</span>
            </div>
            <div className="leader-row">
              <span>Renewals &amp; cancellations</span>
              <span className="leader-fill !border-paper/20" />
              <span className="text-paper">handled</span>
            </div>
          </div>
        </div>

        <p className="relative text-xs text-paper/40">© {new Date().getFullYear()} Ledger Billing</p>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-sm animate-fade-up">
          <Outlet />
        </div>
      </div>

      <Toaster
        position="top-right"
        toastOptions={{
          style: { background: "#12181B", color: "#F7F7F3", fontSize: "13.5px", borderRadius: "10px" },
        }}
      />
    </div>
  );
}
