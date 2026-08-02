import { apiClient } from "./apiClient";

export const authService = {
  register({ username, email, password }) {
    // POST /auth/register — JSON body, returns UserResponse (201)
    return apiClient.post("/auth/register", { username, email, password });
  },

  login({ email, password }) {
    // POST /auth/login — the backend uses OAuth2PasswordRequestForm, so this
    // MUST be sent as application/x-www-form-urlencoded with "username"
    // holding the email. A JSON body will fail validation.
    const body = new URLSearchParams();
    body.append("username", email);
    body.append("password", password);

    return apiClient.post("/auth/login", body, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
  },
};
