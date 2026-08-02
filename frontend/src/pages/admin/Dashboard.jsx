import { useEffect, useState } from "react";
import {
  FiUsers,
  FiLayers,
  FiRepeat,
  FiCreditCard,
} from "react-icons/fi";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import { dashboardService } from "../../services/dashboardService";
import StatCard from "../../components/cards/StatCard";
import Card from "../../components/ui/Card";
import StatusBadge from "../../components/ui/StatusBadge";
import ErrorState from "../../components/ui/ErrorState";
import { SkeletonCard, SkeletonRow } from "../../components/ui/Loader";
import { formatCurrency, formatDateTime, formatDate } from "../../utils/format";

const STATUS_COLORS = { active: "#0E5F5A", expired: "#C1443A", cancelled: "#9CA6A8" };

export default function AdminDashboard() {
  const [summary, setSummary] = useState(null);
  const [revenue, setRevenue] = useState(null);
  const [recentPayments, setRecentPayments] = useState([]);
  const [recentSubs, setRecentSubs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  async function load() {
    setLoading(true);
    setError(false);
    try {
      const [s, r, rp, rs] = await Promise.all([
        dashboardService.getAdminSummary(),
        dashboardService.getRevenueReport(),
        dashboardService.getRecentPayments(6),
        dashboardService.getRecentSubscriptions(6),
      ]);
      setSummary(s.data);
      setRevenue(r.data);
      setRecentPayments(rp.data);
      setRecentSubs(rs.data);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (error) return <ErrorState message="Couldn't load the admin dashboard." onRetry={load} />;

  const statusData = summary
    ? [
        { name: "active", value: summary.active_subscriptions },
        { name: "expired", value: summary.expired_subscriptions },
        { name: "cancelled", value: summary.cancelled_subscriptions },
      ].filter((d) => d.value > 0)
    : [];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="font-display text-2xl text-ink">Console overview</h2>
        <p className="mt-1 text-sm text-ink-faint">Live figures, straight from the ledger.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => <SkeletonCard key={i} />)
        ) : (
          <>
            <StatCard label="Total users" value={summary.total_users} icon={<FiUsers size={16} />} />
            <StatCard label="Plans" value={summary.total_plans} icon={<FiLayers size={16} />} />
            <StatCard label="Subscriptions" value={summary.total_subscriptions} icon={<FiRepeat size={16} />} />
            <StatCard
              label="Total revenue"
              value={summary.total_revenue}
              format="currency"
              icon={<FiCreditCard size={16} />}
              accent
            />
          </>
        )}
      </div>

      <div className="grid gap-4 lg:grid-cols-5">
        <Card className="lg:col-span-2">
          <p className="text-xs font-semibold uppercase tracking-wider text-ink-faint">
            Subscription status
          </p>
          {loading ? (
            <div className="mt-6 h-48 animate-pulse rounded-lg bg-ink/[0.05]" />
          ) : statusData.length === 0 ? (
            <p className="mt-8 text-center text-sm text-ink-faint">No subscriptions yet.</p>
          ) : (
            <div className="mt-2 flex items-center gap-4">
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie data={statusData} dataKey="value" nameKey="name" innerRadius={45} outerRadius={72} paddingAngle={2}>
                    {statusData.map((entry) => (
                      <Cell key={entry.name} fill={STATUS_COLORS[entry.name]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value, name) => [value, name]}
                    contentStyle={{ borderRadius: 10, border: "1px solid #DEDFD6", fontSize: 12 }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
          <div className="mt-3 flex flex-wrap justify-center gap-4">
            {statusData.map((d) => (
              <div key={d.name} className="flex items-center gap-1.5 text-xs text-ink-soft">
                <span className="h-2 w-2 rounded-full" style={{ background: STATUS_COLORS[d.name] }} />
                <span className="capitalize">{d.name}</span>
                <span className="tabular text-ink-faint">{d.value}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="lg:col-span-3">
          <div className="flex items-baseline justify-between">
            <p className="text-xs font-semibold uppercase tracking-wider text-ink-faint">Revenue</p>
            {!loading && (
              <span className="text-xs text-ink-faint tabular">
                {revenue.successful_payments} successful payments
              </span>
            )}
          </div>
          {loading ? (
            <div className="mt-6 h-48 animate-pulse rounded-lg bg-ink/[0.05]" />
          ) : (
            <div className="mt-4">
              <ResponsiveContainer width="100%" height={180}>
                <BarChart
                  data={[
                    { label: "Total revenue", value: revenue.total_revenue },
                    { label: "Average payment", value: revenue.average_payment },
                  ]}
                  layout="vertical"
                  margin={{ left: 8, right: 24 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#EFEFE9" horizontal={false} />
                  <XAxis type="number" hide />
                  <YAxis type="category" dataKey="label" width={120} tick={{ fontSize: 12, fill: "#3C4649" }} axisLine={false} tickLine={false} />
                  <Tooltip
                    formatter={(v) => formatCurrency(v)}
                    contentStyle={{ borderRadius: 10, border: "1px solid #DEDFD6", fontSize: 12 }}
                  />
                  <Bar dataKey="value" fill="#0E5F5A" radius={[0, 6, 6, 0]} barSize={28} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card padded={false}>
          <div className="border-b border-line px-6 py-4">
            <h3 className="font-display text-base text-ink">Recent payments</h3>
          </div>
          <div className="divide-y divide-line px-6">
            {loading &&
              Array.from({ length: 3 }).map((_, i) => <SkeletonRow key={i} />)}
            {!loading && recentPayments.length === 0 && (
              <p className="py-8 text-center text-sm text-ink-faint">No payments yet.</p>
            )}
            {!loading &&
              recentPayments.map((p) => (
                <div key={p.id} className="flex items-center justify-between py-3.5 text-sm">
                  <div>
                    <p className="tabular text-xs text-ink-faint">{p.transaction_id}</p>
                    <p className="text-ink-faint">{formatDateTime(p.payment_date)}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="tabular font-medium text-ink">{formatCurrency(p.amount)}</span>
                    <StatusBadge status={p.payment_status} />
                  </div>
                </div>
              ))}
          </div>
        </Card>

        <Card padded={false}>
          <div className="border-b border-line px-6 py-4">
            <h3 className="font-display text-base text-ink">Recent subscriptions</h3>
          </div>
          <div className="divide-y divide-line px-6">
            {loading &&
              Array.from({ length: 3 }).map((_, i) => <SkeletonRow key={i} />)}
            {!loading && recentSubs.length === 0 && (
              <p className="py-8 text-center text-sm text-ink-faint">No subscriptions yet.</p>
            )}
            {!loading &&
              recentSubs.map((s) => {
                const planName = s?.plan?.plan_name ?? s?.plan_name ?? "Unknown plan";
                return (
                  <div key={s.id} className="flex items-center justify-between py-3.5 text-sm">
                    <div>
                      <p className="text-ink">{planName}</p>
                      <p className="text-ink-faint tabular">{formatDate(s.start_date)}</p>
                    </div>
                    <StatusBadge status={s.status} />
                  </div>
                );
              })}
          </div>
        </Card>
      </div>
    </div>
  );
}
