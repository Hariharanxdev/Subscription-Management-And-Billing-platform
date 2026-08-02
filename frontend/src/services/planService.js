import { apiClient } from "./apiClient";

export const planService = {
  getAll() {
    return apiClient.get("/plans/");
  },
  getById(id) {
    return apiClient.get(`/plans/${id}`);
  },
  create(payload) {
    // { plan_name, description, price, billing_cycle, duration_days }
    return apiClient.post("/plans/", payload);
  },
  update(id, payload) {
    // Full replace — backend has no partial update.
    return apiClient.put(`/plans/${id}`, payload);
  },
  remove(id) {
    return apiClient.delete(`/plans/${id}`);
  },
};
