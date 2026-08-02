import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { FiRepeat, FiXCircle, FiRefreshCw, FiCreditCard, FiCheck } from "react-icons/fi";
import { subscriptionService } from "../../services/subscriptionService";
import { planService } from "../../services/planService";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import StatusBadge from "../../components/ui/StatusBadge";
import EmptyState from "../../components/ui/EmptyState";
import ErrorState from "../../components/ui/ErrorState";
import { SkeletonCard } from "../../components/ui/Loader";
import ConfirmDialog from "../../components/modals/ConfirmDialog";
import { formatCurrency, formatDate, extractErrorMessage } from "../../utils/format";

export default function CustomerSubscription() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [busyId, setBusyId] = useState(null);
  const [confirm, setConfirm] = useState(null); // { type: 'cancel'|'renew', subscription }
  const navigate = useNavigate();

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const [subsRes, plansRes] = await Promise.all([
        subscriptionService.getMine(),
        planService.getAll(),
      ]);
      setSubscriptions(subsRes.data);
      setPlans(plansRes.data.filter((p) => p.is_active));
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const hasActive = subscriptions.some((s) => s.status === "active");

  async function handleSubscribe(planId) {
    setBusyId(planId);
    try {
      await subscriptionService.subscribe(planId);
      toast.success("Subscribed. You can pay for it below whenever you're ready.");
      load();
    } catch (err) {
      toast.error(extractErrorMessage(err));
    } finally {
      setBusyId(null);
    }
  }

  async function handleConfirm() {
    if (!confirm) return;
    setBusyId(confirm.subscription.id);
    try {
      if (confirm.type === "cancel") {
        await subscriptionService.cancel(confirm.subscription.id);
        toast.success("Subscription cancelled.");
      } else {
        await subscriptionService.renew(confirm.subscription.id);
        toast.success("Subscription renewed.");
      }
      setConfirm(null);
      load();
    } catch (err) {
      toast.error(extractErrorMessage(err));
    } finally {
      setBusyId(null);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="font-display text-2xl text-ink">Subscription</h2>
        <p className="mt-1 text-sm text-ink-faint">
          One active subscription at a time. Renew after it expires, cancel whenever you like.
        </p>
      </div>

      {error && <ErrorState message="Couldn't load your subscription." onRetry={load} />}

      {!error && (
        <>
          {/* Current / history */}
          <section className="space-y-3">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-ink-faint">History</h3>

            {loading && (
              <div className="space-y-3">
                <SkeletonCard />
                <SkeletonCard />
              </div>
            )}

            {!loading && subscriptions.length === 0 && (
              <Card>
                <EmptyState
                  icon={<FiRepeat size={20} />}
                  title="No subscriptions yet"
                  description="Choose a plan below to get started."
                />
              </Card>
            )}

            {!loading &&
              subscriptions
                .slice()
                .sort((a, b) => b.id - a.id)
                .map((sub) => (
                  <Card key={sub.id} className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <div className="flex items-center gap-2.5">
                        <h4 className="font-display text-lg text-ink">{sub.plan.plan_name}</h4>
                        <StatusBadge status={sub.status} />
                      </div>
                      <p className="mt-1 text-sm text-ink-faint tabular">
                        {formatDate(sub.start_date)} → {formatDate(sub.end_date)} ·{" "}
                        {formatCurrency(sub.plan.price)}
                      </p>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {sub.status === "active" && (
                        <>
                          <Button
                            variant="secondary"
                            icon={<FiCreditCard size={14} />}
                            onClick={() => navigate("/app/payments", { state: { subscriptionId: sub.id } })}
                          >
                            Pay for this
                          </Button>
                          <Button
                            variant="danger"
                            icon={<FiXCircle size={14} />}
                            loading={busyId === sub.id}
                            onClick={() => setConfirm({ type: "cancel", subscription: sub })}
                          >
                            Cancel
                          </Button>
                        </>
                      )}
                      {sub.status === "expired" && (
                        <Button
                          variant="primary"
                          icon={<FiRefreshCw size={14} />}
                          loading={busyId === sub.id}
                          onClick={() => setConfirm({ type: "renew", subscription: sub })}
                        >
                          Renew
                        </Button>
                      )}
                    </div>
                  </Card>
                ))}
          </section>

          {/* Available plans */}
          <section className="space-y-3">
            <div className="flex items-baseline justify-between">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-ink-faint">
                Available plans
              </h3>
              {hasActive && (
                <p className="text-xs text-ink-faint">You already have an active subscription.</p>
              )}
            </div>

            {loading && (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <SkeletonCard />
                <SkeletonCard />
                <SkeletonCard />
              </div>
            )}

            {!loading && (
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {plans.map((plan) => (
                  <Card key={plan.id} className="flex flex-col">
                    <h4 className="font-display text-lg text-ink">{plan.plan_name}</h4>
                    <p className="mt-1 text-sm text-ink-faint line-clamp-2">{plan.description}</p>
                    <div className="mt-4 flex items-baseline gap-1.5 tabular">
                      <span className="text-2xl font-semibold text-ink">{formatCurrency(plan.price)}</span>
                      <span className="text-xs text-ink-faint">/ {plan.billing_cycle}</span>
                    </div>
                    <p className="mt-1 text-xs text-ink-faint">{plan.duration_days} days</p>
                    <Button
                      className="mt-5 w-full"
                      disabled={hasActive}
                      loading={busyId === plan.id}
                      icon={<FiCheck size={14} />}
                      onClick={() => handleSubscribe(plan.id)}
                    >
                      Subscribe
                    </Button>
                  </Card>
                ))}
              </div>
            )}
          </section>
        </>
      )}

      <ConfirmDialog
        open={Boolean(confirm)}
        onClose={() => setConfirm(null)}
        onConfirm={handleConfirm}
        loading={busyId === confirm?.subscription?.id}
        tone={confirm?.type === "cancel" ? "danger" : "primary"}
        title={confirm?.type === "cancel" ? "Cancel subscription?" : "Renew subscription?"}
        description={
          confirm?.type === "cancel"
            ? "This stops your plan immediately. You can subscribe again later."
            : `This starts a new ${confirm?.subscription?.plan?.plan_name} billing period from today.`
        }
        confirmLabel={confirm?.type === "cancel" ? "Cancel subscription" : "Renew"}
      />
    </div>
  );
}
