import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Topbar from "../components/layout/Topbar";
import { Toaster } from "react-hot-toast";

const TITLES = {
  "/app/dashboard": "Dashboard",
  "/app/subscription": "Subscription",
  "/app/payments": "Payments",
  "/app/invoices": "Invoices",
  "/admin/dashboard": "Overview",
  "/admin/plans": "Subscription plans",
  "/admin/subscriptions": "Subscriptions",
  "/admin/payments": "Payments",
  "/admin/invoices": "Invoices",
  "/admin/users": "Users",
};

export default function AppLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();
  const title = TITLES[location.pathname] || "Ledger";

  return (
    <div className="flex min-h-screen bg-paper">
      <Sidebar mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} />
      <div className="flex min-h-screen flex-1 flex-col min-w-0">
        <Topbar onOpenMobile={() => setMobileOpen(true)} title={title} />
        <main className="flex-1 px-5 py-6 lg:px-8 lg:py-8">
          <div className="mx-auto max-w-6xl animate-fade-up">
            <Outlet />
          </div>
        </main>
      </div>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: "#12181B",
            color: "#F7F7F3",
            fontSize: "13.5px",
            borderRadius: "10px",
          },
        }}
      />
    </div>
  );
}
