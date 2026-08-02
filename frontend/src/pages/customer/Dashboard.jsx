import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FiCreditCard, FiFileText, FiRepeat, FiArrowRight } from "react-icons/fi";
import { dashboardService } from "../../services/dashboardService";
import StatCard from "../../components/cards/StatCard";
import Card from "../../components/ui/Card";
import StatusBadge from "../../components/ui/StatusBadge";
import { SkeletonCard } from "../../components/ui/Loader";
import ErrorState from "../../components/ui/ErrorState";
import { formatCurrency, formatDate, daysUntil } from "../../utils/format";

export default function CustomerDashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data } = await dashboardService.getCustomerSummary();
      setSummary(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (error) return <ErrorState message="Couldn't load your dashboard." onRetry={load} />;

  const sub = summary?.active_subscription;
  const remaining = sub ? daysUntil(sub.end_date) : null;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl text-ink">Your account, at a glance</h2>
        <p className="mt-1 text-sm text-ink-faint">A running total of what you've paid and hold with us.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        {loading ? (
          <>
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
          </>
        ) : (
          <>
            <StatCard
              label="Total paid"
              value={summary.total_amount_paid}
              format="currency"
              icon={<FiCreditCard size={16} />}
            />
            <StatCard label="Payments made" value={summary.total_payments} icon={<FiRepeat size={16} />} />
            <StatCard label="Invoices issued" value={summary.total_invoices} icon={<FiFileText size={16} />} />
          </>
        )}
      </div>

      <Card>
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-ink-faint">
              Current subscription
            </p>
            {loading ? (
              <div className="mt-2 h-6 w-40 animate-pulse rounded bg-ink/[0.06]" />
            ) : sub ? (
              <h3 className="mt-1 font-display text-xl text-ink">{sub.plan_name}</h3>
            ) : (
              <h3 className="mt-1 font-display text-xl text-ink">No active subscription</h3>
            )}
          </div>
          {!loading && sub && <StatusBadge status={sub.status} />}
        </div>

        {!loading && sub && (
          <div className="mt-5 space-y-2">
            <div className="leader-row text-sm text-ink-soft">
              <span>Plan price</span>
              <span className="leader-fill" />
              <span className="tabular text-ink">{formatCurrency(sub.price)}</span>
            </div>
            <div className="leader-row text-sm text-ink-soft">
              <span>Started</span>
              <span className="leader-fill" />
              <span className="tabular text-ink">{formatDate(sub.start_date)}</span>
            </div>
            <div className="leader-row text-sm text-ink-soft">
              <span>Renews / ends</span>
              <span className="leader-fill" />
              <span className="tabular text-ink">
                {formatDate(sub.end_date)}
                {remaining !== null && remaining >= 0 && (
                  <span className="ml-1.5 text-xs text-ink-faint">({remaining}d left)</span>
                )}
              </span>
            </div>
          </div>
        )}

        {!loading && !sub && (
          <p className="mt-3 text-sm text-ink-faint">
            You don't have a subscription right now. Choose a plan to get started.
          </p>
        )}

        <Link
          to="/app/subscription"
          className="mt-5 inline-flex items-center gap-1.5 text-sm font-medium text-ledger-600 hover:underline"
        >
          Manage subscription <FiArrowRight size={14} />
        </Link>
      </Card>
    </div>
  );
}
