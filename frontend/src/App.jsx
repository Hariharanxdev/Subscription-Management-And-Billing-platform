import { Routes, Route, Navigate } from "react-router-dom";
import { NotificationProvider } from "./context/NotificationContext";

import PublicLayout from "./layouts/PublicLayout";
import AuthLayout from "./layouts/AuthLayout";
import AppLayout from "./layouts/AppLayout";

import ProtectedRoute from "./routes/ProtectedRoute";
import AdminRoute from "./routes/AdminRoute";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import PlansMarketing from "./pages/public/PlansMarketing";

import CustomerDashboard from "./pages/customer/Dashboard";
import CustomerSubscription from "./pages/customer/Subscription";
import CustomerPayments from "./pages/customer/Payments";
import CustomerInvoices from "./pages/customer/Invoices";
import CustomerProfile from "./pages/customer/Profile";

import AdminDashboard from "./pages/admin/Dashboard";
import AdminPlans from "./pages/admin/Plans";
import AdminSubscriptions from "./pages/admin/Subscriptions";
import AdminPayments from "./pages/admin/Payments";
import AdminInvoices from "./pages/admin/Invoices";
import AdminUsers from "./pages/admin/Users";

import NotFound from "./pages/public/NotFound";

export default function App() {
  return (
    <NotificationProvider>
      <Routes>
        {/* Public */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<PlansMarketing />} />
          <Route path="/plans" element={<Navigate to="/" replace />} />
        </Route>

        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>

        {/* Customer */}
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/app/dashboard" element={<CustomerDashboard />} />
            <Route path="/app/subscription" element={<CustomerSubscription />} />
            <Route path="/app/payments" element={<CustomerPayments />} />
            <Route path="/app/invoices" element={<CustomerInvoices />} />
            <Route path="/app/profile" element={<CustomerProfile />} />

            {/* Admin */}
            <Route element={<AdminRoute />}>
              <Route path="/admin/dashboard" element={<AdminDashboard />} />
              <Route path="/admin/plans" element={<AdminPlans />} />
              <Route path="/admin/subscriptions" element={<AdminSubscriptions />} />
              <Route path="/admin/payments" element={<AdminPayments />} />
              <Route path="/admin/invoices" element={<AdminInvoices />} />
              <Route path="/admin/users" element={<AdminUsers />} />
            </Route>
          </Route>
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </NotificationProvider>
  );
}
