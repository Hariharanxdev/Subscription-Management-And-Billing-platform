export const TOKEN_KEY = "ledger_access_token";

export const ROLES = {
  ADMIN: "admin",
  USER: "user",
};

export const SUBSCRIPTION_STATUS = {
  ACTIVE: "active",
  CANCELLED: "cancelled",
  EXPIRED: "expired",
};

export const PAYMENT_METHODS = [
  { value: "upi", label: "UPI" },
  { value: "card", label: "Credit / Debit Card" },
  { value: "netbanking", label: "Net Banking" },
  { value: "wallet", label: "Wallet" },
];

export const NOTIFICATION_LABELS = {
  payment_success: { label: "Payment", tone: "success" },
  subscription_cancelled: { label: "Cancelled", tone: "muted" },
  subscription_expired: { label: "Expired", tone: "danger" },
  subscription_renewed: { label: "Renewed", tone: "success" },
  expiry_reminder: { label: "Reminder", tone: "warning" },
};
