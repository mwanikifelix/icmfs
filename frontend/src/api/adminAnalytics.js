import api from "@/services/api";

export function fetchAdminAnalytics() {
  return api.get("/admin_panel/analytics/");
}
