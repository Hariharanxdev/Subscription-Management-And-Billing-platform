import axios from "axios";
import toast from "react-hot-toast";
import { tokenStorage } from "../utils/tokenStorage";
import { extractErrorMessage } from "../utils/format";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const apiClient = axios.create({
  baseURL: BASE_URL,
});

// Attach the bearer token to every outgoing request.
apiClient.interceptors.request.use((config) => {
  const token = tokenStorage.get();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// One place to react to auth failures and surface a consistent error message.
let onUnauthorized = null;
export function registerUnauthorizedHandler(handler) {
  onUnauthorized = handler;
}

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;

    // 401: token missing/invalid/expired. 403 "inactive account": force logout too.
    const detail = error?.response?.data?.detail;
    const isInactive = typeof detail === "string" && detail.toLowerCase().includes("inactive");

    if (status === 401 || (status === 403 && isInactive)) {
      if (onUnauthorized) onUnauthorized();
    }

    return Promise.reject(error);
  }
);

export function apiErrorToast(error, fallback) {
  toast.error(extractErrorMessage(error) || fallback);
}
