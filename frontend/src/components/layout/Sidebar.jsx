import { NavLink } from "react-router-dom";
import clsx from "clsx";
import {
  FiGrid,
  FiLayers,
  FiRepeat,
  FiCreditCard,
  FiFileText,
  FiUsers,
  FiX,
} from "react-icons/fi";
import { useAuth } from "../../context/AuthContext";

const customerNav = [
  { to: "/app/dashboard", label: "Dashboard", icon: FiGrid },
  { to: "/app/subscription", label: "Subscription", icon: FiRepeat },
  { to: "/app/payments", label: "Payments", icon: FiCreditCard },
  { to: "/app/invoices", label: "Invoices", icon: FiFileText },
];

const adminNav = [
  { to: "/admin/dashboard", label: "Overview", icon: FiGrid },
  { to: "/admin/plans", label: "Plans", icon: FiLayers },
  { to: "/admin/subscriptions", label: "Subscriptions", icon: FiRepeat },
  { to: "/admin/payments", label: "Payments", icon: FiCreditCard },
  { to: "/admin/invoices", label: "Invoices", icon: FiFileText },
  { to: "/admin/users", label: "Users", icon: FiUsers },
];

function NavItem({ to, label, icon: Icon }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        clsx(
          "group relative flex items-center gap-3 rounded-lg px-3.5 py-2.5 text-sm font-medium transition-colors",
          isActive ? "text-ledger-600" : "text-ink-soft hover:text-ink hover:bg-ink/[0.03]"
        )
      }
    >
      {({ isActive }) => (
        <>
          {isActive && (
            <span className="absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-full bg-gold-500" />
          )}
          <Icon size={17} className={isActive ? "text-ledger-500" : "text-ink-faint group-hover:text-ink-soft"} />
          {label}
        </>
      )}
    </NavLink>
  );
}

export default function Sidebar({ mobileOpen, onCloseMobile }) {
  const { isAdmin } = useAuth();
  const items = isAdmin ? adminNav : customerNav;

  const content = (
    <>
      <div className="flex items-center gap-2.5 px-5 py-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-ledger-500">
          <svg width="16" height="16" viewBox="0 0 32 32" fill="none">
            <path d="M9 12h14M9 16h14M9 20h9" stroke="#F7F7F3" strokeWidth="2.4" strokeLinecap="round" />
          </svg>
        </div>
        <div>
          <p className="font-display text-[15px] font-semibold leading-none text-ink">Ledger</p>
          <p className="text-[11px] text-ink-faint tracking-wide mt-0.5">
            {isAdmin ? "Admin console" : "Billing"}
          </p>
        </div>
        <button className="ml-auto lg:hidden text-ink-faint" onClick={onCloseMobile}>
          <FiX size={18} />
        </button>
      </div>
      <nav className="flex-1 space-y-0.5 px-3">
        {items.map((item) => (
          <NavItem key={item.to} {...item} />
        ))}
      </nav>
      <div className="mx-5 mb-5 mt-4 rounded-xl border border-line bg-paper-dim/60 p-3.5">
        <p className="text-[11px] font-semibold uppercase tracking-wider text-ink-faint">
          {isAdmin ? "Console" : "Plan"}
        </p>
        <p className="mt-1 text-xs text-ink-soft leading-relaxed">
          {isAdmin
            ? "Every figure here reads straight from the ledger — no cached numbers."
            : "Manage your plan, invoices and payment history in one place."}
        </p>
      </div>
    </>
  );

  return (
    <>
      {/* Desktop */}
      <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r lg:border-line lg:bg-white/70 lg:backdrop-blur-sm">
        {content}
      </aside>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="absolute inset-0 bg-ink/40" onClick={onCloseMobile} />
          <aside className="absolute left-0 top-0 flex h-full w-72 flex-col bg-white shadow-pop animate-fade-up">
            {content}
          </aside>
        </div>
      )}
    </>
  );
}
