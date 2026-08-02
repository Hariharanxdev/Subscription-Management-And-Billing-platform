import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";
import { authService } from "../services/authService";
import { registerUnauthorizedHandler } from "../services/apiClient";
import { tokenStorage } from "../utils/tokenStorage";
import { decodeToken, isTokenExpired } from "../utils/jwt";

const AuthContext = createContext(null);

function userFromToken(token) {
  const payload = decodeToken(token);
  if (!payload) return null;
  // The JWT only carries { sub: email, role, exp } — no id/username exists
  // anywhere in the backend for the signed-in user, so email is the identity.
  return { email: payload.sub, role: payload.role };
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => {
    const stored = tokenStorage.get();
    return stored && !isTokenExpired(stored) ? stored : null;
  });
  const [initializing, setInitializing] = useState(true);

  const user = useMemo(() => userFromToken(token), [token]);

  const logout = useCallback((message) => {
    tokenStorage.clear();
    setToken(null);
    if (message) toast.error(message);
  }, []);

  useEffect(() => {
    registerUnauthorizedHandler(() => {
      logout("Your session has ended. Please sign in again.");
    });
  }, [logout]);

  useEffect(() => {
    if (token && isTokenExpired(token)) {
      logout();
    }
    setInitializing(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = useCallback(async (email, password) => {
    const { data } = await authService.login({ email, password });
    tokenStorage.set(data.access_token);
    setToken(data.access_token);
    return userFromToken(data.access_token);
  }, []);

  const register = useCallback(async (payload) => {
    await authService.register(payload);
  }, []);

  const value = useMemo(
    () => ({
      token,
      user,
      isAuthenticated: Boolean(user),
      isAdmin: user?.role === "admin",
      initializing,
      login,
      register,
      logout,
    }),
    [token, user, initializing, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
