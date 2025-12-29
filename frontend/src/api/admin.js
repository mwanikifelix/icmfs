import api from "./client";

/* USERS */
export const fetchUsers = () =>
  api.get("/api/admin_panel/users/");

export const createUser = (payload) =>
  api.post("/api/admin_panel/users/create/", payload);

/* ROLES */
export const fetchRoles = () =>
  api.get("/api/admin_panel/roles/");

/* AUDIT LOGS */
export const fetchAuditLogs = () =>
  api.get("/api/admin_panel/audit-logs/");
