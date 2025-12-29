import api from "./api";

/* USERS */
export const fetchUsers = () => api.get("/admin_panel/users/");
export const createUser = (data) => api.post("/admin_panel/users/create/", data);
export const updateUser = (id, data) =>
  api.put(`/admin_panel/users/${id}/`, data);

/* ROLES */
export const fetchRoles = () => api.get("/admin_panel/roles/");

/* PERMISSIONS */
export const fetchPermissions = () => api.get("/admin_panel/permissions/");
