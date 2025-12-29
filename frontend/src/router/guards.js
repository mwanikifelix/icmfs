import api from "@/services/api";

export async function adminGuard(to, from, next) {
  if (!to.meta.requiresAdmin) return next();

  try {
    const res = await api.get("/admin_panel/me/");
    if (res.data.is_staff) next();
    else next("/dashboard");
  } catch {
    next("/login");
  }
}
