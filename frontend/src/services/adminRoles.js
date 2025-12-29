import api from "./api";

export const fetchRoles = () =>
  api.get("/admin_panel/roles/");

export const createRole = (data) =>
  api.post("/admin_panel/roles/", data);

export const updateRole = (id, data) =>
  api.put(`/admin_panel/roles/${id}/`, data);

export const fetchPermissions = () =>
  api.get("/admin_panel/permissions/");
