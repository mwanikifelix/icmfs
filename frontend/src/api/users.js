import api from "./client";

/* List users */
export const fetchUsers = () =>
  api.get("/api/admin_panel/users/");

/* Create user */
export const createUser = (data) =>
  api.post("/api/admin_panel/users/", data);

/* Update user */
export const updateUser = (id, data) =>
  api.put(`/api/admin_panel/users/${id}/`, data);

/* Toggle active */
export const toggleUserStatus = (id) =>
  api.patch(`/api/admin_panel/users/${id}/toggle-active/`);
