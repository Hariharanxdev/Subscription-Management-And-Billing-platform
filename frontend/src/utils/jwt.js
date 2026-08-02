import { jwtDecode } from "jwt-decode";

/**
 * The backend JWT payload only ever contains: { sub: <email>, role, exp }.
 * There is no user id or username in the token, and no /auth/me endpoint,
 * so email + role is all the frontend can know about the signed-in user.
 */
export function decodeToken(token) {
  if (!token) return null;
  try {
    const payload = jwtDecode(token);
    return payload;
  } catch {
    return null;
  }
}

export function isTokenExpired(token) {
  const payload = decodeToken(token);
  if (!payload?.exp) return true;
  return payload.exp * 1000 < Date.now();
}
