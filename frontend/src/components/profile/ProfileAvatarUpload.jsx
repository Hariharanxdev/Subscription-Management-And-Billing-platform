import { useRef } from "react";
import { FiCamera } from "react-icons/fi";

/**
 * Shows the current avatar (uploaded image or initials fallback) with a
 * camera button to pick a new one. The file is only read into a local data
 * URL via FileReader and handed back through onChange — nothing is uploaded
 * anywhere yet, since there's no backend endpoint for it.
 */
export default function ProfileAvatarUpload({ avatarUrl, initials, onChange, size = 88 }) {
  const inputRef = useRef(null);

  function handleFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) return;
    if (file.size > 4 * 1024 * 1024) return; // 4MB soft cap for local preview

    const reader = new FileReader();
    reader.onload = () => onChange?.(reader.result);
    reader.readAsDataURL(file);
    e.target.value = "";
  }

  return (
    <div className="relative inline-flex" style={{ width: size, height: size }}>
      {avatarUrl ? (
        <img
          src={avatarUrl}
          alt="Profile"
          className="h-full w-full rounded-full object-cover border border-line"
          style={{ width: size, height: size }}
        />
      ) : (
        <div
          className="flex items-center justify-center rounded-full bg-ledger-500 font-display font-semibold text-paper"
          style={{ width: size, height: size, fontSize: size * 0.36 }}
        >
          {initials}
        </div>
      )}

      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        className="absolute bottom-0 right-0 flex h-8 w-8 items-center justify-center rounded-full bg-white text-ink-soft border border-line shadow-card hover:text-ledger-600 hover:border-ledger-400"
        aria-label="Change profile picture"
      >
        <FiCamera size={14} />
      </button>
      <input ref={inputRef} type="file" accept="image/*" className="hidden" onChange={handleFile} />
    </div>
  );
}
