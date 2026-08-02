import { apiClient } from "./apiClient";

export const paymentService = {
  create({ subscriptionId, paymentMethod }) {
    return apiClient.post("/payments/", {
      subscription_id: subscriptionId,
      payment_method: paymentMethod,
    });
  },
  getAll() {
    return apiClient.get("/payments/");
  },
  getById(id) {
    return apiClient.get(`/payments/${id}`);
  },
  getBySubscription(subscriptionId) {
    return apiClient.get(`/payments/subscription/${subscriptionId}`);
  },
};
