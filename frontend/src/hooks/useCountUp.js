import { useEffect, useRef, useState } from "react";

/**
 * Animates a number from 0 up to `value` like an odometer. Used on dashboard
 * KPI cards — the platform's one recurring motion signature.
 */
export function useCountUp(value, { duration = 700 } = {}) {
  const [display, setDisplay] = useState(0);
  const frame = useRef(null);

  useEffect(() => {
    const end = Number(value) || 0;
    const start = 0;
    const startTime = performance.now();

    function tick(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(start + (end - start) * eased);
      if (progress < 1) {
        frame.current = requestAnimationFrame(tick);
      } else {
        setDisplay(end);
      }
    }

    frame.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame.current);
  }, [value, duration]);

  return display;
}
