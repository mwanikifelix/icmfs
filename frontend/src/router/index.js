/* import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';
import TestAPI from '@/views/TestAPI.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: '/uikit/formlayout',
                    name: 'formlayout',
                    component: () => import('@/views/uikit/FormLayout.vue')
                },
                {
                    path: '/uikit/input',
                    name: 'input',
                    component: () => import('@/views/uikit/InputDoc.vue')
                },
                {
                    path: '/uikit/button',
                    name: 'button',
                    component: () => import('@/views/uikit/ButtonDoc.vue')
                },
                {
                    path: '/uikit/table',
                    name: 'table',
                    component: () => import('@/views/uikit/TableDoc.vue')
                },
                {
                    path: '/uikit/list',
                    name: 'list',
                    component: () => import('@/views/uikit/ListDoc.vue')
                },
                {
                    path: '/uikit/tree',
                    name: 'tree',
                    component: () => import('@/views/uikit/TreeDoc.vue')
                },
                {
                    path: '/uikit/panel',
                    name: 'panel',
                    component: () => import('@/views/uikit/PanelsDoc.vue')
                },

                {
                    path: '/uikit/overlay',
                    name: 'overlay',
                    component: () => import('@/views/uikit/OverlayDoc.vue')
                },
                {
                    path: '/uikit/media',
                    name: 'media',
                    component: () => import('@/views/uikit/MediaDoc.vue')
                },
                {
                    path: '/uikit/message',
                    name: 'message',
                    component: () => import('@/views/uikit/MessagesDoc.vue')
                },
                {
                    path: '/uikit/file',
                    name: 'file',
                    component: () => import('@/views/uikit/FileDoc.vue')
                },
                {
                    path: '/uikit/menu',
                    name: 'menu',
                    component: () => import('@/views/uikit/MenuDoc.vue')
                },
                {
                    path: '/uikit/charts',
                    name: 'charts',
                    component: () => import('@/views/uikit/ChartDoc.vue')
                },
                {
                    path: '/uikit/misc',
                    name: 'misc',
                    component: () => import('@/views/uikit/MiscDoc.vue')
                },
                {
                    path: '/uikit/timeline',
                    name: 'timeline',
                    component: () => import('@/views/uikit/TimelineDoc.vue')
                },
                {
                    path: '/blocks/free',
                    name: 'blocks',
                    meta: {
                        breadcrumb: ['Prime Blocks', 'Free Blocks']
                    },
                    component: () => import('@/views/utilities/Blocks.vue')
                },
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                {
                    path: '/pages/crud',
                    name: 'crud',
                    component: () => import('@/views/pages/Crud.vue')
                },
                {
                    path: '/start/documentation',
                    name: 'documentation',
                    component: () => import('@/views/pages/Documentation.vue')
                }
            ]
        },
        {
            path: '/landing',
            name: 'landing',
            component: () => import('@/views/pages/Landing.vue')
        },
        {
            path: '/pages/notfound',
            name: 'notfound',
            component: () => import('@/views/pages/NotFound.vue')
        },

        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        },

        {
          path: '/test-api',
          name: 'test-api',
          component: TestAPI
        },
    ]
});

export default router;
 */



import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  // ========== PUBLIC ROUTES ==========
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/public/Home.vue'),
    meta: { public: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/public/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/public/Register.vue'),
    meta: { public: true }
  },

  // ========== AUTHENTICATED LAYOUT ==========
  {
    path: '/app',
    component: () => import('@/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/app/dashboard',
    children: [
      // DASHBOARD
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { requiresAuth: true }
      },

      // PROJECTS
      {
        path: 'projects',
        meta: { requiresAuth: true },
        children: [
          {
            path: '',
            name: 'projects',
            component: () => import('@/views/projects/ProjectList.vue')
          },
          {
            path: 'create',
            name: 'project-create',
            component: () => import('@/views/projects/ProjectCreate.vue')
          },
          {
            path: ':id',
            name: 'project-overview',
            component: () => import('@/views/projects/ProjectOverview.vue')
          },
          {
            path: ':id/edit',
            name: 'project-edit',
            component: () => import('@/views/projects/ProjectEdit.vue')
          }
        ]
      },

      // PROGRESS
      {
        path: 'progress',
        meta: { requiresAuth: true },
        children: [
          {
            path: 'overview',
            name: 'progress-overview',
            component: () => import('@/views/progress/ProgressOverview.vue')
          },
          {
            path: 'reports',
            name: 'daily-reports',
            component: () => import('@/views/progress/DailyReports.vue')
          },
          {
            path: 'evm',
            name: 'evm-analysis',
            component: () => import('@/views/progress/EVMAnalysis.vue')
          }
        ]
      },

      // FINANCE
      {
        path: 'finance',
        meta: { requiresAuth: true },
        children: [
          {
            path: 'dashboard',
            name: 'finance-dashboard',
            component: () => import('@/views/finance/FinanceDashboard.vue')
          },
          {
            path: 'expenses',
            name: 'expenses',
            component: () => import('@/views/finance/Expenses.vue')
          },
          {
            path: 'payments',
            name: 'payments',
            component: () => import('@/views/finance/Payments.vue')
          }
        ]
      },

      // QA
      {
        path: 'qa',
        meta: { requiresAuth: true },
        children: [
          {
            path: 'issues',
            name: 'qa-issues',
            component: () => import('@/views/qa/QAIssues.vue')
          },
          {
            path: 'inspection',
            name: 'qa-inspection',
            component: () => import('@/views/qa/QAInspection.vue')
          }
        ]
      },

      // AI
      {
        path: 'ai',
        meta: { requiresAuth: true },
        children: [
          {
            path: 'assistant',
            name: 'ai-assistant',
            component: () => import('@/views/ai/AIAssistant.vue')
          },
          {
            path: 'insights',
            name: 'ai-insights',
            component: () => import('@/views/ai/AIInsights.vue')
          }
        ]
      },

      // ACCOUNT
      {
        path: 'profile',
        name: 'profile',
        component: () => import('@/views/account/Profile.vue'),
        meta: { requiresAuth: true }
      },

      // ADMIN (Protected)
      {
        path: 'admin',
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
          {
            path: 'dashboard',
            name: 'admin-dashboard',
            component: () => import('@/views/admin/AdminDashboard.vue')
          },
          {
            path: 'users',
            name: 'admin-users',
            component: () => import('@/views/admin/Users.vue')
          },
          {
            path: 'roles',
            name: 'admin-roles',
            component: () => import('@/views/admin/Roles.vue')
          }
        ]
      }
    ]
  },

  // 404 Not Found
  {
    path: '/:pathMatch(.*)*',
    name: 'notfound',
    component: () => import('@/views/NotFound.vue')
  }
];

// Create the router
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// ========== NAVIGATION GUARDS ==========
router.beforeEach((to, from, next) => {
  // Get authentication state
  const isAuthenticated = !!localStorage.getItem('token');
  const userRole = localStorage.getItem('role');
  const isAdmin = userRole === 'admin';

  // Allow public routes
  if (to.meta.public) {
    // If already logged in, redirect to dashboard
    if (isAuthenticated && (to.name === 'login' || to.name === 'register')) {
      next('/app/dashboard');
    } else {
      next();
    }
    return;
  }

  // Check authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({
      path: '/login',
      query: { redirect: to.fullPath } // Save intended destination
    });
    return;
  }

  // Check admin access
  if (to.meta.requiresAdmin && !isAdmin) {
    next('/app/dashboard');
    return;
  }

  // Allow navigation
  next();
});

// Optional: After navigation hook for analytics, page titles, etc.
router.afterEach((to) => {
  // Set page title
  document.title = to.meta.title || 'ICMFS - Integrated Construction Management System';
  
  // You can add analytics tracking here
  // analytics.track('page_view', { path: to.path });
});

export default router;