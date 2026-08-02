import { useEffect } from "react";
import { createPortal } from "react-dom";
import { FiX } from "react-icons/fi";

export default function Modal({ open, onClose, title, children, size = "md" }) {
  useEffect(() => {
    if (!open) return;
    function onKey(e) {
      if (e.key === "Escape") onClose?.();
    }
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, onClose]);

  if (!open) return null;

  const widths = { sm: "max-w-sm", md: "max-w-md", lg: "max-w-lg", xl: "max-w-2xl" };

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-ink/40 backdrop-blur-[2px] animate-fade-up"
        onClick={onClose}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className={`relative w-full ${widths[size]} rounded-xl2 bg-white shadow-pop border border-line animate-fade-up`}
      >
        <div className="flex items-center justify-between border-b border-line px-6 py-4">
          <h3 className="text-lg font-semibold text-ink font-display">{title}</h3>
          <button
            onClick={onClose}
            className="rounded-full p-1.5 text-ink-faint hover:bg-ink/5 hover:text-ink"
            aria-label="Close"
          >
            <FiX size={18} />
          </button>
        </div>
        <div className="px-6 py-5">{children}</div>
      </div>
    </div>,
    document.body
  );
}
