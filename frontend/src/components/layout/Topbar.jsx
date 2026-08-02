import { useNavigate } from "react-router-dom";
import { FiMenu, FiBell, FiChevronDown, FiLogOut } from "react-icons/fi";
import { useAuth } from "../../context/AuthContext";
import { useNotifications } from "../../context/NotificationContext";
import Avatar from "../ui/Avatar";
import Dropdown from "../ui/Dropdown";
import { NOTIFICATION_LABELS } from "../../constants";
import { formatDateTime } from "../../utils/format";

export default function Topbar({ onOpenMobile, title }) {
  const { user, logout } = useAuth();
  const { notifications, unreadCount, markAsRead } = useNotifications();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-30 flex items-center gap-4 border-b border-line bg-paper/85 backdrop-blur px-5 py-4 lg:px-8">
      <button className="lg:hidden text-ink-soft" onClick={onOpenMobile} aria-label="Open menu">
        <FiMenu size={20} />
      </button>

      <h1 className="font-display text-lg text-ink truncate">{title}</h1>

      <div className="ml-auto flex items-center gap-2">
        <Dropdown
          trigger={
            <button
              className="relative flex h-9 w-9 items-center justify-center rounded-full text-ink-soft hover:bg-ink/5"
              aria-label="Notifications"
            >
              <FiBell size={18} />
              {unreadCount > 0 && (
                <span className="absolute -top-0.5 -right-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-brick-500 px-1 text-[10px] font-semibold text-white">
                  {unreadCount}
                </span>
              )}
            </button>
          }
        >
          <div className="max-h-96 w-80 overflow-y-auto">
            <div className="px-4 py-2 text-xs font-semibold uppercase tracking-wider text-ink-faint">
              Notifications
            </div>
            {notifications.length === 0 && (
              <p className="px-4 py-6 text-center text-sm text-ink-faint">You're all caught up.</p>
            )}
            {notifications.slice(0, 8).map((n) => {
              const meta = NOTIFICATION_LABELS[n.notification_type] || { label: n.notification_type };
              return (
                <button
                  key={n.id}
                  onClick={(e) => {
                    e.stopPropagation();
                    if (!n.is_read) markAsRead(n.id);
                  }}
                  className="flex w-full flex-col gap-0.5 border-b border-line/70 px-4 py-3 text-left last:border-0 hover:bg-ink/[0.02]"
                >
                  <div className="flex items-center gap-2">
                    {!n.is_read && <span className="h-1.5 w-1.5 rounded-full bg-gold-500" />}
                    <span className="text-sm font-medium text-ink">{n.title}</span>
                    <span className="text-[10px] font-semibold uppercase tracking-wide text-ink-faint">
                      {meta.label}
                    </span>
                  </div>
                  <p className="text-xs text-ink-faint line-clamp-2">{n.message}</p>
                  <p className="text-[11px] text-ink-faint/80 tabular">{formatDateTime(n.created_at)}</p>
                </button>
              );
            })}
          </div>
        </Dropdown>

        <Dropdown
          trigger={
            <button className="flex items-center gap-2 rounded-full py-1 pl-1 pr-2.5 hover:bg-ink/5">
              <Avatar email={user?.email} size={30} />
              <span className="hidden sm:block text-sm text-ink-soft max-w-[140px] truncate">
                {user?.email}
              </span>
              <FiChevronDown size={14} className="text-ink-faint hidden sm:block" />
            </button>
          }
        >
          <div className="px-4 py-2 border-b border-line">
            <p className="text-sm font-medium text-ink truncate">{user?.email}</p>
            <p className="text-xs text-ink-faint capitalize">{user?.role}</p>
          </div>
          <button
            onClick={() => {
              logout();
              navigate("/login");
            }}
            className="flex w-full items-center gap-2 px-4 py-2.5 text-sm text-brick-500 hover:bg-brick-500/5"
          >
            <FiLogOut size={15} /> Sign out
          </button>
        </Dropdown>
      </div>
    </header>
  );
}
