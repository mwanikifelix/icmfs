import api from "./client";

/* Fetch all roles */
export const fetchRoles = () =>
  api.get("/api/admin_panel/roles/");

/* Fetch all permissions */
export const fetchPermissions = () =>
  api.get("/api/admin_panel/permissions/");

/* Fetch permissions for a role */
export const fetchRolePermissions = (roleId) =>
  api.get(`/api/admin_panel/roles/${roleId}/permissions/`);

/* Update permissions for a role */
export const updateRolePermissions = (roleId, permissions) =>
  api.put(`/api/admin_panel/roles/${roleId}/permissions/`, {
    permissions,
  });
