import { apiClient } from "./apiClient";

export const subscriptionService = {
  subscribe(planId) {
    return apiClient.post("/subscriptions/", { plan_id: planId });
  },
  getMine() {
    return apiClient.get("/subscriptions/me");
  },
  getAll() {
    return apiClient.get("/subscriptions/");
  },
  renew(subscriptionId) {
    return apiClient.post(`/subscriptions/${subscriptionId}/renew`);
  },
  cancel(subscriptionId) {
    return apiClient.put(`/subscriptions/${subscriptionId}/cancel`);
  },
  checkExpired() {
    return apiClient.post("/subscriptions/check-expired");
  },
};
