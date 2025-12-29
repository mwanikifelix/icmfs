import api from "./api";

export const getAdminStats = async () => {
  const [
    users,
    projects,
    qa,
    notifications,
    audits,
  ] = await Promise.all([
    api.get("/accounts/users/"),
    api.get("/projects/"),
    api.get("/qa/"),
    api.get("/notifications/"),
    api.get("/admin_panel/audit-logs/"),
  ]);

  return {
    users: users.data.length,
    projects: projects.data.length,
    activeProjects: projects.data.filter(p => p.status === "active").length,
    pendingQA: qa.data.filter(q => q.status === "pending").length,
    notifications: notifications.data.length,
    auditLogs: audits.data.length,
  };
};
