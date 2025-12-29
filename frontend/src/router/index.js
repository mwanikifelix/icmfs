


import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
 {
  path: "/",
  meta: { requiresAuth: true },
  children: [
    {
      path: "dashboard",
      name: "Dashboard",
      
      component: () => import("@/views/dashboard/Dashboard.vue"),
    },

    // 🔹 PLACEHOLDERS (safe)
   {
  path: "/login",
  name: "Login",
  meta: { public: true },
  component: () => import("@/views/auth/Login.vue"),
},


    {
      path: "projects",
      component: () => import("@/views/projects/ProjectList.vue"),
    },
    {
      path: "progress",
      component: () => import("@/views/progress/ProgressOverview.vue"),
    },
    {
      path: "finance",
      component: () => import("@/views/finance/FinanceDashboard.vue"),
    },
    {
      path: "qa",
      component: () => import("@/views/qa/QAList.vue"),
    },
    {
      path: "notifications",
      component: () =>
        import("@/views/notifications/NotificationList.vue"),
    },
    {
      path: "ai",
      component: () => import("@/views/ai/Assistant.vue"),
    },

    // Account
    {
      path: "account/profile",
      component: () => import("@/views/account/Profile.vue"),
    },
    {
      path: "account/security",
      component: () => import("@/views/account/Security.vue"),
    },
    {
      path: "account/preferences",
      component: () => import("@/views/account/Preferences.vue"),
    },

    {
      path: "",
      redirect: "/dashboard",
    },
  ]

 }
  ]




const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();

  // Public route
  if (to.path === "/login") {
    if (auth.isAuthenticated) {
      return "/dashboard";
    }
    return true;
  }

  // Protected routes
  if (!auth.isAuthenticated) {
    return "/login";
  }

  return true;
});


export default router;
