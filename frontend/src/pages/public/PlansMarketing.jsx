import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FiCheck } from "react-icons/fi";
import { planService } from "../../services/planService";
import { useAuth } from "../../context/AuthContext";
import { formatCurrency } from "../../utils/format";
import { SkeletonCard } from "../../components/ui/Loader";
import ErrorState from "../../components/ui/ErrorState";
import toast from "react-hot-toast";

export default function PlansMarketing() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const { isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data } = await planService.getAll();
      setPlans(data.filter((p) => p.is_active));
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  function handleChoose() {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }
    if (isAdmin) {
      toast("Admin accounts don't hold subscriptions — sign in as a customer.");
      return;
    }
    navigate("/app/subscription");
  }

  return (
    <div>
      <div className="max-w-2xl">
        <p className="text-xs font-semibold uppercase tracking-wider text-ledger-500">Pricing</p>
        <h1 className="mt-2 text-4xl font-display text-ink leading-[1.1]">
          Simple plans, kept in the ledger.
        </h1>
        <p className="mt-4 text-ink-faint">
          Every plan renews on a fixed cycle, bills automatically, and generates a paper trail —
          an invoice for every payment, a notification for every change.
        </p>
      </div>

      {error && <ErrorState message="Couldn't load plans." onRetry={load} />}

      {!error && (
        <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {loading &&
            Array.from({ length: 3 }).map((_, i) => <SkeletonCard key={i} />)}

          {!loading &&
            plans.map((plan, i) => (
              <div
                key={plan.id}
                className={`card p-6 flex flex-col animate-fade-up ${
                  i === 1 ? "border-ledger-500 ring-1 ring-ledger-500" : ""
                }`}
                style={{ animationDelay: `${i * 60}ms` }}
              >
                {i === 1 && (
                  <span className="mb-3 inline-flex w-fit items-center rounded-full bg-ledger-50 px-2.5 py-1 text-[11px] font-semibold text-ledger-600">
                    Most chosen
                  </span>
                )}
                <h3 className="font-display text-xl text-ink">{plan.plan_name}</h3>
                <p className="mt-1.5 text-sm text-ink-faint">{plan.description}</p>

                <div className="mt-5 flex items-baseline gap-1.5 tabular">
                  <span className="text-3xl font-semibold text-ink">
                    {formatCurrency(plan.price)}
                  </span>
                  <span className="text-sm text-ink-faint">/ {plan.billing_cycle}</span>
                </div>

                <div className="mt-4 leader-row text-sm text-ink-soft">
                  <span>Billing cycle</span>
                  <span className="leader-fill" />
                  <span className="tabular">{plan.duration_days} days</span>
                </div>
                <div className="mt-2 flex items-center gap-2 text-sm text-ink-soft">
                  <FiCheck className="text-ledger-500 shrink-0" size={15} />
                  Automatic invoice on payment
                </div>
                <div className="mt-1.5 flex items-center gap-2 text-sm text-ink-soft">
                  <FiCheck className="text-ledger-500 shrink-0" size={15} />
                  Cancel or renew anytime
                </div>

                <button onClick={handleChoose} className="btn-primary mt-6 w-full">
                  Choose {plan.plan_name}
                </button>
              </div>
            ))}
        </div>
      )}

      {!loading && !error && plans.length === 0 && (
        <p className="mt-10 text-sm text-ink-faint">No plans are available right now.</p>
      )}

      {!isAuthenticated && (
        <p className="mt-10 text-sm text-ink-faint">
          Already have an account?{" "}
          <Link to="/login" className="font-medium text-ledger-600 hover:underline">
            Sign in
          </Link>
        </p>
      )}
    </div>
  );
}
