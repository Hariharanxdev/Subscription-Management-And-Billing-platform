import { forwardRef, useState } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";
import clsx from "clsx";

const PasswordInput = forwardRef(function PasswordInput(
  { label, error, hint, className, id, ...props },
  ref
) {
  const [visible, setVisible] = useState(false);
  const inputId = id || props.name;

  return (
    <div className="space-y-1.5">
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-ink-soft">
          {label}
        </label>
      )}
      <div className="relative">
        <input
          ref={ref}
          id={inputId}
          type={visible ? "text" : "password"}
          className={clsx(
            "input pr-10",
            error && "border-brick-500 focus:border-brick-500",
            className
          )}
          {...props}
        />
        <button
          type="button"
          tabIndex={-1}
          onClick={() => setVisible((v) => !v)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint hover:text-ink-soft"
          aria-label={visible ? "Hide password" : "Show password"}
        >
          {visible ? <FiEyeOff size={16} /> : <FiEye size={16} />}
        </button>
      </div>
      {error && <p className="text-xs text-brick-500">{error}</p>}
      {!error && hint && <p className="text-xs text-ink-faint">{hint}</p>}
    </div>
  );
});

export default PasswordInput;
