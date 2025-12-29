import api from "./api";

export function login(payload) {
  return api.post("/token/", payload);
}

export function refreshToken(refresh) {
  return api.post("/token/refresh/", { refresh });
}
