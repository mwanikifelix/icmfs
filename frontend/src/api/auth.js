import api from "@/services/api";

export const login = (credentials) => {
  return api.post("/accounts/login/", credentials);
};

export const refreshToken = (data) => {
  return api.post("/accounts/token/refresh/", data);
};
