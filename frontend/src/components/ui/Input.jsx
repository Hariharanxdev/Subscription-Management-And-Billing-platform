import { forwardRef } from "react";
import clsx from "clsx";

const Input = forwardRef(function Input(
  { label, error, hint, className, id, ...props },
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
      <input
        ref={ref}
        id={inputId}
        className={clsx(
          "input",
          error && "border-brick-500 focus:border-brick-500",
          className
        )}
        {...props}
      />
      {error && <p className="text-xs text-brick-500">{error}</p>}
      {!error && hint && <p className="text-xs text-ink-faint">{hint}</p>}
    </div>
  );
});

export default Input;
