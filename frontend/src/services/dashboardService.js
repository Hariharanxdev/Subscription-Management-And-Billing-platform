import { apiClient } from "./apiClient";

export const dashboardService = {
  getAdminSummary() {
    return apiClient.get("/dashboard/admin/summary");
  },
  getRecentPayments(limit = 5) {
    return apiClient.get("/dashboard/admin/recent-payments", { params: { limit } });
  },
  getRecentSubscriptions(limit = 5) {
    return apiClient.get("/dashboard/admin/recent-subscriptions", { params: { limit } });
  },
  getRevenueReport() {
    return apiClient.get("/dashboard/admin/revenue");
  },
  getCustomerSummary() {
    return apiClient.get("/dashboard/customer/summary");
  },
};
