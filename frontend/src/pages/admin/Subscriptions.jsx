import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { FiRefreshCw } from "react-icons/fi";
import { subscriptionService } from "../../services/subscriptionService";
import DataTable from "../../components/tables/DataTable";
import FilterPanel from "../../components/tables/FilterPanel";
import StatusBadge from "../../components/ui/StatusBadge";
import Button from "../../components/ui/Button";
import ErrorState from "../../components/ui/ErrorState";
import { formatCurrency, formatDate, extractErrorMessage } from "../../utils/format";

const STATUS_OPTIONS = [
  { value: "all", label: "All" },
  { value: "active", label: "Active" },
  { value: "expired", label: "Expired" },
  { value: "cancelled", label: "Cancelled" },
];

export default function AdminSubscriptions() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [statusFilter, setStatusFilter] = useState("all");
  const [checking, setChecking] = useState(false);

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data } = await subscriptionService.getAll();
      setSubscriptions(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleCheckExpired() {
    setChecking(true);
    try {
      const { data } = await subscriptionService.checkExpired();
      toast.success(`${data.updated_count} subscription(s) marked expired.`);
      load();
    } catch (err) {
      toast.error(extractErrorMessage(err));
    } finally {
      setChecking(false);
    }
  }

  const filtered =
    statusFilter === "all" ? subscriptions : subscriptions.filter((s) => s.status === statusFilter);

  const columns = [
    { key: "id", header: "ID", render: (r) => <span className="tabular">#{r.id}</span> },
    { key: "user_id", header: "User ID", render: (r) => <span className="tabular">#{r.user_id}</span> },
    { key: "plan_name", header: "Plan", sortable: true, sortValue: (r) => r.plan.plan_name, render: (r) => r.plan.plan_name },
    { key: "price", header: "Price", sortValue: (r) => r.plan.price, render: (r) => <span className="tabular">{formatCurrency(r.plan.price)}</span> },
    { key: "start_date", header: "Start", sortable: true, render: (r) => <span className="tabular">{formatDate(r.start_date)}</span> },
    { key: "end_date", header: "End", sortable: true, render: (r) => <span className="tabular">{formatDate(r.end_date)}</span> },
    { key: "status", header: "Status", render: (r) => <StatusBadge status={r.status} /> },
  ];

  if (error) return <ErrorState message="Couldn't load subscriptions." onRetry={load} />;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="font-display text-2xl text-ink">Subscriptions</h2>
          <p className="mt-1 text-sm text-ink-faint">Every subscription across all customers.</p>
        </div>
        <Button variant="secondary" icon={<FiRefreshCw size={14} />} loading={checking} onClick={handleCheckExpired}>
          Run expiry check
        </Button>
      </div>

      <FilterPanel options={STATUS_OPTIONS} value={statusFilter} onChange={setStatusFilter} />

      <DataTable
        columns={columns}
        data={filtered}
        loading={loading}
        searchKeys={["id", "user_id"]}
        searchPlaceholder="Search by ID…"
        emptyState={<p className="py-12 text-center text-sm text-ink-faint">No subscriptions found.</p>}
      />
    </div>
  );
}
