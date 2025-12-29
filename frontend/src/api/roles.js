import api from "./client";

/* List roles */
export const fetchRoles = () =>
  api.get("/api/admin_panel/roles/");

/* Create role */
export const createRole = (data) =>
  api.post("/api/admin_panel/roles/", data);
