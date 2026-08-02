import clsx from "clsx";

export default function Card({ className, children, padded = true, ...props }) {
  return (
    <div className={clsx("card", padded && "p-6", className)} {...props}>
      {children}
    </div>
  );
}
