import { useEffect, useState } from "react";
import { paymentService } from "../../services/paymentService";
import DataTable from "../../components/tables/DataTable";
import FilterPanel from "../../components/tables/FilterPanel";
import StatusBadge from "../../components/ui/StatusBadge";
import ErrorState from "../../components/ui/ErrorState";
import { formatCurrency, formatDateTime } from "../../utils/format";

const STATUS_OPTIONS = [
  { value: "all", label: "All" },
  { value: "success", label: "Success" },
  { value: "pending", label: "Pending" },
  { value: "failed", label: "Failed" },
];

export default function AdminPayments() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [statusFilter, setStatusFilter] = useState("all");

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data } = await paymentService.getAll();
      setPayments(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const filtered =
    statusFilter === "all" ? payments : payments.filter((p) => p.payment_status === statusFilter);

  const columns = [
    { key: "id", header: "ID", render: (r) => <span className="tabular">#{r.id}</span> },
    { key: "subscription_id", header: "Subscription", render: (r) => <span className="tabular">#{r.subscription_id}</span> },
    { key: "transaction_id", header: "Transaction ID", render: (r) => <span className="tabular text-xs">{r.transaction_id}</span> },
    { key: "payment_method", header: "Method", render: (r) => <span className="capitalize">{r.payment_method}</span> },
    { key: "amount", header: "Amount", sortable: true, render: (r) => <span className="tabular font-medium text-ink">{formatCurrency(r.amount)}</span> },
    { key: "payment_status", header: "Status", render: (r) => <StatusBadge status={r.payment_status} /> },
    { key: "payment_date", header: "Date", sortable: true, render: (r) => <span className="tabular">{formatDateTime(r.payment_date)}</span> },
  ];

  if (error) return <ErrorState message="Couldn't load payments." onRetry={load} />;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl text-ink">Payments</h2>
        <p className="mt-1 text-sm text-ink-faint">Every payment captured across all customers.</p>
      </div>

      <FilterPanel options={STATUS_OPTIONS} value={statusFilter} onChange={setStatusFilter} />

      <DataTable
        columns={columns}
        data={filtered}
        loading={loading}
        searchKeys={["transaction_id", "payment_method"]}
        searchPlaceholder="Search by transaction ID…"
        emptyState={<p className="py-12 text-center text-sm text-ink-faint">No payments found.</p>}
      />
    </div>
  );
}
