import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { FiPlus, FiEdit2, FiTrash2, FiLayers } from "react-icons/fi";
import { planService } from "../../services/planService";
import DataTable from "../../components/tables/DataTable";
import Button from "../../components/ui/Button";
import ErrorState from "../../components/ui/ErrorState";
import PlanFormModal from "../../components/modals/PlanFormModal";
import ConfirmDialog from "../../components/modals/ConfirmDialog";
import { formatCurrency, formatDate, extractErrorMessage } from "../../utils/format";

export default function AdminPlans() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [formOpen, setFormOpen] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);
  const [deletingPlan, setDeletingPlan] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data } = await planService.getAll();
      setPlans(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  function openCreate() {
    setEditingPlan(null);
    setFormOpen(true);
  }

  function openEdit(plan) {
    setEditingPlan(plan);
    setFormOpen(true);
  }

  async function handleSubmit(values) {
    setSubmitting(true);
    try {
      if (editingPlan) {
        await planService.update(editingPlan.id, values);
        toast.success("Plan updated.");
      } else {
        await planService.create(values);
        toast.success("Plan created.");
      }
      setFormOpen(false);
      load();
    } catch (err) {
      toast.error(extractErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete() {
    if (!deletingPlan) return;
    setSubmitting(true);
    try {
      await planService.remove(deletingPlan.id);
      toast.success("Plan deleted.");
      setDeletingPlan(null);
      load();
    } catch (err) {
      toast.error(extractErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  }

  const columns = [
    { key: "plan_name", header: "Plan", sortable: true, render: (r) => <span className="font-medium text-ink">{r.plan_name}</span> },
    { key: "description", header: "Description", render: (r) => <span className="text-ink-faint line-clamp-1 max-w-xs block">{r.description}</span> },
    { key: "price", header: "Price", sortable: true, render: (r) => <span className="tabular">{formatCurrency(r.price)}</span> },
    { key: "billing_cycle", header: "Cycle", render: (r) => <span className="capitalize">{r.billing_cycle}</span> },
    { key: "duration_days", header: "Days", sortable: true, render: (r) => <span className="tabular">{r.duration_days}</span> },
    {
      key: "is_active",
      header: "Status",
      render: (r) => (
        <span className={r.is_active ? "badge-active" : "badge-cancelled"}>{r.is_active ? "active" : "inactive"}</span>
      ),
    },
    { key: "created_at", header: "Created", render: (r) => <span className="tabular">{formatDate(r.created_at)}</span> },
    {
      key: "actions",
      header: "",
      render: (r) => (
        <div className="flex gap-1.5">
          <button
            className="rounded-lg p-1.5 text-ink-faint hover:bg-ink/5 hover:text-ledger-600"
            onClick={() => openEdit(r)}
            aria-label="Edit plan"
          >
            <FiEdit2 size={14} />
          </button>
          <button
            className="rounded-lg p-1.5 text-ink-faint hover:bg-brick-500/10 hover:text-brick-500"
            onClick={() => setDeletingPlan(r)}
            aria-label="Delete plan"
          >
            <FiTrash2 size={14} />
          </button>
        </div>
      ),
    },
  ];

  if (error) return <ErrorState message="Couldn't load plans." onRetry={load} />;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 className="font-display text-2xl text-ink">Subscription plans</h2>
          <p className="mt-1 text-sm text-ink-faint">Create, edit, and retire plans customers can subscribe to.</p>
        </div>
        <Button icon={<FiPlus size={15} />} onClick={openCreate}>
          New plan
        </Button>
      </div>

      <DataTable
        columns={columns}
        data={plans}
        loading={loading}
        searchKeys={["plan_name", "billing_cycle"]}
        searchPlaceholder="Search plans…"
        emptyState={
          <div className="py-12 text-center">
            <FiLayers className="mx-auto mb-2 text-ink-faint" size={22} />
            <p className="text-sm text-ink-faint">No plans yet — create your first one.</p>
          </div>
        }
      />

      <PlanFormModal
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSubmit={handleSubmit}
        submitting={submitting}
        initialValues={editingPlan}
      />

      <ConfirmDialog
        open={Boolean(deletingPlan)}
        onClose={() => setDeletingPlan(null)}
        onConfirm={handleDelete}
        loading={submitting}
        tone="danger"
        title="Delete this plan?"
        description={`"${deletingPlan?.plan_name}" will be permanently removed. This doesn't affect existing subscriptions.`}
        confirmLabel="Delete plan"
      />
    </div>
  );
}
