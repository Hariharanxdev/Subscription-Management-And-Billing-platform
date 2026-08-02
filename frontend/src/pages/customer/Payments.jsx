import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import toast from "react-hot-toast";
import { FiCreditCard } from "react-icons/fi";
import { subscriptionService } from "../../services/subscriptionService";
import { paymentService } from "../../services/paymentService";
import DataTable from "../../components/tables/DataTable";
import StatusBadge from "../../components/ui/StatusBadge";
import Button from "../../components/ui/Button";
import ErrorState from "../../components/ui/ErrorState";
import PayNowModal from "../../components/modals/PayNowModal";
import { formatCurrency, formatDateTime, extractErrorMessage } from "../../utils/format";

export default function CustomerPayments() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedSub, setSelectedSub] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const location = useLocation();

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data: subs } = await subscriptionService.getMine();
      setSubscriptions(subs);

      const results = await Promise.all(
        subs.map((s) => paymentService.getBySubscription(s.id).then((r) => r.data))
      );
      const merged = results.flat().map((p) => ({
        ...p,
        plan_name: subs.find((s) => s.id === p.subscription_id)?.plan?.plan_name || "—",
      }));
      merged.sort((a, b) => new Date(b.payment_date) - new Date(a.payment_date));
      setPayments(merged);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  // Arrived from Subscription page's "Pay for this" button.
  useEffect(() => {
    const subId = location.state?.subscriptionId;
    if (subId && subscriptions.length > 0) {
      const sub = subscriptions.find((s) => s.id === subId);
      if (sub) openPayModal(sub);
      window.history.replaceState({}, document.title);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [subscriptions]);

  const paidSubscriptionIds = new Set(
    payments.filter((p) => p.payment_status === "success").map((p) => p.subscription_id)
  );
  const payableSubscriptions = subscriptions.filter(
    (s) => s.status === "active" && !paidSubscriptionIds.has(s.id)
  );

  function openPayModal(sub) {
    setSelectedSub(sub);
    setSuccess(false);
    setModalOpen(true);
  }

  async function handlePay(paymentMethod) {
    if (!selectedSub) return;
    setSubmitting(true);
    try {
      await paymentService.create({ subscriptionId: selectedSub.id, paymentMethod });
      setSuccess(true);
      toast.success("Payment successful.");
      load();
      setTimeout(() => setModalOpen(false), 1400);
    } catch (err) {
      toast.error(extractErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  }

  const columns = [
    {
      key: "payment_date",
      header: "Date",
      sortable: true,
      render: (r) => <span className="tabular">{formatDateTime(r.payment_date)}</span>,
    },
    { key: "plan_name", header: "Plan", sortable: true },
    {
      key: "transaction_id",
      header: "Transaction ID",
      render: (r) => <span className="tabular text-xs">{r.transaction_id}</span>,
    },
    { key: "payment_method", header: "Method", render: (r) => <span className="capitalize">{r.payment_method}</span> },
    {
      key: "amount",
      header: "Amount",
      sortable: true,
      render: (r) => <span className="tabular font-medium text-ink">{formatCurrency(r.amount)}</span>,
    },
    { key: "payment_status", header: "Status", render: (r) => <StatusBadge status={r.payment_status} /> },
  ];

  if (error) return <ErrorState message="Couldn't load your payments." onRetry={load} />;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="font-display text-2xl text-ink">Payments</h2>
          <p className="mt-1 text-sm text-ink-faint">Every payment you've made, with its transaction ID.</p>
        </div>
        {payableSubscriptions.length > 0 && (
          <Button icon={<FiCreditCard size={15} />} onClick={() => openPayModal(payableSubscriptions[0])}>
            Pay now
          </Button>
        )}
      </div>

      <DataTable
        columns={columns}
        data={payments}
        loading={loading}
        searchKeys={["plan_name", "transaction_id", "payment_method"]}
        searchPlaceholder="Search payments…"
        emptyState={
          <div className="py-12 text-center">
            <p className="text-sm text-ink-faint">No payments yet.</p>
          </div>
        }
      />

      <PayNowModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        subscription={selectedSub}
        onSubmit={handlePay}
        submitting={submitting}
        success={success}
      />
    </div>
  );
}
