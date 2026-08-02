import clsx from "clsx";

const VARIANTS = {
  primary: "btn-primary",
  secondary: "btn-secondary",
  ghost: "btn-ghost",
  danger: "btn-danger",
};

export default function Button({
  variant = "primary",
  loading = false,
  icon,
  className,
  children,
  disabled,
  ...props
}) {
  return (
    <button
      className={clsx(VARIANTS[variant], className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <span className="h-4 w-4 rounded-full border-2 border-current border-t-transparent animate-spin" />
      ) : (
        icon
      )}
      {children}
    </button>
  );
}
