import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { FiUserCheck, FiUserX } from "react-icons/fi";
import { adminUserService } from "../../services/adminUserService";
import DataTable from "../../components/tables/DataTable";
import FilterPanel from "../../components/tables/FilterPanel";
import Button from "../../components/ui/Button";
import ErrorState from "../../components/ui/ErrorState";
import ConfirmDialog from "../../components/modals/ConfirmDialog";
import { formatDate, extractErrorMessage } from "../../utils/format";

const ROLE_OPTIONS = [
  { value: "all", label: "All" },
  { value: "user", label: "Customers" },
  { value: "admin", label: "Admins" },
];

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [roleFilter, setRoleFilter] = useState("all");
  const [target, setTarget] = useState(null); // { user, action: 'activate'|'deactivate' }
  const [submitting, setSubmitting] = useState(false);

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const { data } = await adminUserService.getAll();
      setUsers(data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleConfirm() {
    if (!target) return;
    setSubmitting(true);
    try {
      if (target.action === "activate") {
        await adminUserService.activate(target.user.id);
        toast.success("User activated.");
      } else {
        await adminUserService.deactivate(target.user.id);
        toast.success("User deactivated.");
      }
      setTarget(null);
      load();
    } catch (err) {
      toast.error(extractErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  }

  const filtered = roleFilter === "all" ? users : users.filter((u) => u.role === roleFilter);

  const columns = [
    { key: "id", header: "ID", render: (r) => <span className="tabular">#{r.id}</span> },
    { key: "username", header: "Username", sortable: true, render: (r) => <span className="font-medium text-ink">{r.username}</span> },
    { key: "email", header: "Email", sortable: true },
    { key: "role", header: "Role", render: (r) => <span className="capitalize">{r.role}</span> },
    {
      key: "is_active",
      header: "Status",
      render: (r) => (
        <span className={r.is_active ? "badge-active" : "badge-expired"}>
          {r.is_active ? "active" : "inactive"}
        </span>
      ),
    },
    { key: "created_at", header: "Joined", sortable: true, render: (r) => <span className="tabular">{formatDate(r.created_at)}</span> },
    {
      key: "actions",
      header: "",
      render: (r) =>
        r.role === "admin" ? (
          <span className="text-xs text-ink-faint">—</span>
        ) : r.is_active ? (
          <Button
            variant="danger"
            className="!px-3 !py-1.5 !text-xs"
            icon={<FiUserX size={13} />}
            onClick={() => setTarget({ user: r, action: "deactivate" })}
          >
            Deactivate
          </Button>
        ) : (
          <Button
            variant="secondary"
            className="!px-3 !py-1.5 !text-xs"
            icon={<FiUserCheck size={13} />}
            onClick={() => setTarget({ user: r, action: "activate" })}
          >
            Activate
          </Button>
        ),
    },
  ];

  if (error) return <ErrorState message="Couldn't load users." onRetry={load} />;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl text-ink">Users</h2>
        <p className="mt-1 text-sm text-ink-faint">Activate or deactivate customer accounts.</p>
      </div>

      <FilterPanel options={ROLE_OPTIONS} value={roleFilter} onChange={setRoleFilter} />

      <DataTable
        columns={columns}
        data={filtered}
        loading={loading}
        searchKeys={["username", "email"]}
        searchPlaceholder="Search by name or email…"
        emptyState={<p className="py-12 text-center text-sm text-ink-faint">No users found.</p>}
      />

      <ConfirmDialog
        open={Boolean(target)}
        onClose={() => setTarget(null)}
        onConfirm={handleConfirm}
        loading={submitting}
        tone={target?.action === "deactivate" ? "danger" : "primary"}
        title={target?.action === "deactivate" ? "Deactivate this user?" : "Activate this user?"}
        description={
          target?.action === "deactivate"
            ? `"${target?.user?.username}" will be signed out and unable to log back in until reactivated.`
            : `"${target?.user?.username}" will regain access immediately.`
        }
        confirmLabel={target?.action === "deactivate" ? "Deactivate" : "Activate"}
      />
    </div>
  );
}
