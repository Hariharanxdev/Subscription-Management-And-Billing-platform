export default function Avatar({ email, size = 36 }) {
  const initial = email ? email[0].toUpperCase() : "?";
  return (
    <div
      className="flex items-center justify-center rounded-full bg-ledger-500 font-display font-semibold text-paper"
      style={{ width: size, height: size, fontSize: size * 0.4 }}
    >
      {initial}
    </div>
  );
}
