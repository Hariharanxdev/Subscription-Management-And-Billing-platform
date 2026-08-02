import { forwardRef } from "react";
import { FiChevronDown } from "react-icons/fi";
import clsx from "clsx";

const Select = forwardRef(function Select(
  { label, error, options = [], placeholder, className, id, ...props },
  ref
) {
  const inputId = id || props.name;
  return (
    <div className="space-y-1.5">
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-ink-soft">
          {label}
        </label>
      )}
      <div className="relative">
        <select
          ref={ref}
          id={inputId}
          className={clsx(
            "input appearance-none pr-9 cursor-pointer",
            error && "border-brick-500 focus:border-brick-500",
            className
          )}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        <FiChevronDown
          className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint"
          size={16}
        />
      </div>
      {error && <p className="text-xs text-brick-500">{error}</p>}
    </div>
  );
});

export default Select;
