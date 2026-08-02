export function formatCurrency(amount) {
  const value = Number(amount ?? 0);
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(value);
}

export function formatDate(value) {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export function formatDateTime(value) {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function daysUntil(dateStr) {
  if (!dateStr) return null;
  const target = new Date(dateStr);
  const today = new Date();
  target.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);
  return Math.round((target - today) / (1000 * 60 * 60 * 24));
}

/**
 * Normalizes FastAPI's two error shapes into a single readable string:
 *  - {"detail": "message"}
 *  - {"detail": [{"loc": [...], "msg": "...", "type": "..."}]}  (422 validation)
 */
export function extractErrorMessage(error) {
  const detail = error?.response?.data?.detail;

  if (!detail) {
    if (error?.message === "Network Error") {
      return "Can't reach the server. Check that the backend is running.";
    }
    return "Something went wrong. Please try again.";
  }

  if (typeof detail === "string") return detail;

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        const field = Array.isArray(item.loc) ? item.loc.at(-1) : "";
        return field ? `${field}: ${item.msg}` : item.msg;
      })
      .join(" · ");
  }

  return "Something went wrong. Please try again.";
}
