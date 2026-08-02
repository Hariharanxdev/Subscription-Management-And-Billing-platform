import { FiAlertTriangle } from "react-icons/fi";
import Button from "./Button";

export default function ErrorState({ message = "Couldn't load this data.", onRetry }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 px-6 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-brick-500/10 text-brick-500">
        <FiAlertTriangle size={20} />
      </div>
      <p className="text-sm text-ink-soft max-w-sm">{message}</p>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry}>
          Try again
        </Button>
      )}
    </div>
  );
}
