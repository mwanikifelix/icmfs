import api from "./api";

export const fetchRoles = () =>
  api.get("/admin_panel/roles/");

export const fetchPermissions = () =>
  api.get("/admin_panel/permissions/");

export const updateRolePermissions = (roleId, permissions) =>
  api.put(`/admin_panel/roles/${roleId}/`, {
    permissions,
  });
