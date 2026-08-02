import clsx from "clsx";

export default function FilterPanel({ options, value, onChange }) {
  return (
    <div className="flex flex-wrap items-center gap-1.5">
      {options.map((opt) => (
        <button
          key={opt.value}
          onClick={() => onChange(opt.value)}
          className={clsx(
            "rounded-full border px-3 py-1.5 text-xs font-medium capitalize transition-colors",
            value === opt.value
              ? "border-ledger-500 bg-ledger-500 text-paper"
              : "border-line bg-white text-ink-soft hover:border-ledger-300"
          )}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}
