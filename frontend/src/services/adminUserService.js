import { apiClient } from "./apiClient";

export const adminUserService = {
  getAll() {
    return apiClient.get("/admin/users/");
  },
  getById(id) {
    return apiClient.get(`/admin/users/${id}`);
  },
  deactivate(id) {
    return apiClient.put(`/admin/users/${id}/deactivate`);
  },
  activate(id) {
    return apiClient.put(`/admin/users/${id}/activate`);
  },
};
