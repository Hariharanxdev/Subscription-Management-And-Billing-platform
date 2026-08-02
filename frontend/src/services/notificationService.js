import { apiClient } from "./apiClient";

export const notificationService = {
  getMine() {
    return apiClient.get("/notifications/me");
  },
  getUnread() {
    return apiClient.get("/notifications/me/unread");
  },
  markAsRead(id) {
    return apiClient.put(`/notifications/${id}/read`);
  },
};
