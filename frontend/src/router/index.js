import { createRouter, createWebHistory } from 'vue-router';

const routes = [

  // ================= ROOT =================
  {
    path: '/',
    redirect: '/login'
  },

  // ================= PUBLIC ROUTES =================
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/public/About.vue'),
    meta: { public: true }
  },
  {
    path: '/contact',
    name: 'contact',
    component: () => import('@/views/public/Contact.vue'),
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
  {
    path: '/password-recovery',
    name: 'password-recovery',
    component: () => import('@/views/public/PasswordRecovery.vue'),
    meta: { public: true }
  },

  // ================= AUTHENTICATED LAYOUT =================
  {
    path: '/app',
    component: () => import('@/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    redirect: '/app/dashboard',
    children: [

      // ================= DASHBOARD =================
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { requiresAuth: true }
      },

      // ================= REGIONS =================
      {
        path: 'regions',
        children: [
          {
            path: '',
            name: 'regions',
            component: () => import('@/views/regions/RegionList.vue')
          },
          {
            path: ':id',
            name: 'region-overview',
            component: () => import('@/views/regions/RegionOverview.vue')
          },
          {
            path: 'counties',
            name: 'counties',
            component: () => import('@/views/regions/CountyList.vue')
          }
        ]
      },

      // ================= PROJECTS =================
      {
        path: 'projects',
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
          }
        ]
      },
      {
        path: 'projects/:id/edit',
        name: 'project-edit',
        component: () => import('@/views/projects/ProjectEdit.vue'),
      },
      
      {
        path: 'projects/:id',
        component: () => import('@/views/projects/ProjectDetail.vue'),
        children: [
          {
            path: '',
            name: 'project-detail',
            component: () => import('@/views/projects/ProjectOverview.vue')
          },
         
          {
            path: 'timeline',
            name: 'project-timeline',
            component: () => import('@/views/projects/ProjectTimeline.vue')
          },
          {
            path: 'media',
            name: 'project-media',
            component: () => import('@/views/projects/ProjectMedia.vue')
          },
          {
            path: 'risks',
            name: 'project-risks',
            component: () => import('@/views/projects/ProjectRisks.vue')
          },
          {
            path: 'reports',
            name: 'project-reports',
            component: () => import('@/views/projects/ProjectReports.vue')
          }
        ]
      },

      // ================= SITES =================
      {
        path: 'sites',
        children: [
          {
            path: '',
            name: 'sites',
            component: () => import('@/views/sites/SiteList.vue')
          },
          {
            path: 'create',
            name: 'site-create',
            component: () => import('@/views/sites/SiteCreate.vue')
          },
          {
            path: ':id',
            name: 'site-detail',
            component: () => import('@/views/sites/SiteDetail.vue')
          },
          {
            path: 'daily-reports',
            name: 'site-daily-reports',
            component: () => import('@/views/sites/DailyReports.vue')
          },
          {
            path: 'workforce',
            name: 'site-workforce',
            component: () => import('@/views/sites/WorkforceManagement.vue')
          }
        ]
      },

      // ================= FINANCE =================
      {
        path: 'finance',
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
            path: 'budget',
            name: 'budget-tracking',
            component: () => import('@/views/finance/BudgetTracking.vue')
          },
          {
            path: 'reports',
            name: 'financial-reports',
            component: () => import('@/views/finance/FinancialReports.vue')
          }
        ]
      },

      // ================= PAYMENTS =================
      {
        path: 'payments',
        children: [
          {
            path: 'dashboard',
            name: 'payment-dashboard',
            component: () => import('@/views/payments/PaymentsDashboard.vue')
          },
          {
            path: 'mpesa',
            name: 'mpesa-payments',
            component: () => import('@/views/payments/ MpesaPayments.vue')
          },
          {
            path: 'mpesa-transactions',
            name: 'mpesa-transactions',
            component: () => import('@/views/payments/MpesaTransactions.vue')
          },
          {
            path: 'bank',
            name: 'bank-payments',
            component: () => import('@/views/payments/BankPayments.vue')
          },
          {
            path: 'approvals',
            name: 'payment-approvals',
            component: () => import('@/views/payments/PaymentApprovals.vue')
          },
          {
            path: 'audit',
            name: 'payment-audit',
            component: () => import('@/views/payments/PaymentAudit.vue')
          },
          {
            path: 'reconciliation',
            name: 'payment-reconciliation',
            component: () => import('@/views/payments/PaymentReconciliation.vue')
          }
        ]
      },

      // ================= PROGRESS =================
      {
        path: 'progress',
        children: [
          {
            path: 'overview',
            name: 'progress-overview',
            component: () => import('@/views/progress/ProgressOverview.vue')
          },
          {
            path: 'daily-logs',
            name: 'daily-logs',
            component: () => import('@/views/progress/DailyLogs.vue')
          },
          {
            path: 'daily-reports',
            name: 'daily-reports',
            component: () => import('@/views/progress/DailyReports.vue')
          },
          {
            path: 'evm',
            name: 'evm-analysis',
            component: () => import('@/views/progress/EVMAnalysis.vue')
          },
          {
            path: 'trends',
            name: 'performance-trends',
            component: () => import('@/views/progress/PerformanceTrends.vue')
          }
        ]
      },

      // ================= PROCUREMENT =================
      {
        path: 'procurement',
        children: [
          {
            path: 'dashboard',
            name: 'procurement-dashboard',
            component: () => import('@/views/procurement/ProcurementDashboard.vue')
          },
          {
            path: 'requests',
            name: 'purchase-requests',
            component: () => import('@/views/procurement/PurchaseRequests.vue')
          },
          {
            path: 'supplier-management',
            name: 'supplier-management',
            component: () => import('@/views/procurement/SupplierManagement.vue')
          },
          {
            path: 'inventory',
            name: 'inventory',
            component: () => import('@/views/procurement/Inventory.vue')
          }
        ]
      },

      // ================= SUPPLIERS =================
      {
        path: 'suppliers',
        children: [
          {
            path: '',
            name: 'supplier-list',
            component: () => import('@/views/suppliers/SupplierList.vue')
          },
          {
            path: 'orders',
            name: 'purchase-orders',
            component: () => import('@/views/suppliers/PurchaseOrders.vue')
          },
          {
            path: 'deliveries',
            name: 'deliveries',
            component: () => import('@/views/suppliers/Deliveries.vue')
          },
          {
            path: 'invoices',
            name: 'supplier-invoices',
            component: () => import('@/views/suppliers/SupplierInvoices.vue')
          },
          {
            path: 'payments',
            name: 'supplier-payments',
            component: () => import('@/views/suppliers/SupplierPayments.vue')
          }
        ]
      },

      // ================= QA =================
      {
        path: 'qa',
        children: [
          {
            path: '',
            name: 'qa-list',
            component: () => import('@/views/qa/QAList.vue')
          },
          {
            path: 'issues',
            name: 'qa-issues',
            component: () => import('@/views/qa/QAIssues.vue')
          },
          {
            path: 'inspections',
            name: 'qa-inspections',
            component: () => import('@/views/qa/QAInspections.vue')
          },
          {
            path: 'certification',
            name: 'qa-certification',
            component: () => import('@/views/qa/QACertification.vue')
          },
          {
            path: 'reports',
            name: 'qa-reports',
            component: () => import('@/views/qa/QAReports.vue')
          }
        ]
      },

      // ================= SAFETY =================
      {
        path: 'safety',
        children: [
          {
            path: 'dashboard',
            name: 'safety-dashboard',
            component: () => import('@/views/safety/Safetydashboard.vue')
          },
          {
            path: 'incidents',
            name: 'incident-reports',
            component: () => import('@/views/safety/IncidentReports.vue')
          },
          {
            path: 'assessments',
            name: 'risk-assessments',
            component: () => import('@/views/safety/RiskAssessments.vue')
          },
          {
            path: 'audits',
            name: 'safety-audits',
            component: () => import('@/views/safety/SafetyAudits.vue')
          }
        ]
      },

      // ================= AI & ANALYTICS =================
      {
        path: 'ai',
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
          },
          {
            path: 'finance',
            name: 'ai-finance-insights',
            component: () => import('@/views/ai/AIFinanceInsights.vue')
          },
          {
            path: 'risks',
            name: 'ai-risk-predictions',
            component: () => import('@/views/ai/AIRiskPredictions.vue')
          }
        ]
      },

      // ================= NOTIFICATIONS =================
      {
        path: 'notifications',
        children: [
          {
            path: 'list',
            name: 'notifications',
            component: () => import('@/views/notifications/NotificationList.vue')
          },
          {
            path: 'settings',
            name: 'notification-settings',
            component: () => import('@/views/notifications/NotificationSettings.vue')
          }
        ]
      },

      // ================= TASKS =================
      /* {
        path: 'tasks',
        name: 'tasks',
        component: () => import('@/views/tasks/Tasks.vue')
      }, */

      // ================= ACCOUNT =================
      {
        path: 'account',
        children: [
          {
            path: 'profile',
            name: 'account-profile',
            component: () => import('@/views/account/Profile.vue')
          },
          {
            path: 'security',
            name: 'account-security',
            component: () => import('@/views/account/Security.vue')
          },
          {
            path: 'preferences',
            name: 'account-preferences',
            component: () => import('@/views/account/Preferences.vue')
          }
        ]
      },

      // ================= ADMIN =================
      {
        path: 'admin',
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
            path: 'user-management',
            name: 'user-management',
            component: () => import('@/views/admin/UserManagement.vue')
          },
          {
            path: 'roles',
            name: 'admin-roles',
            component: () => import('@/views/admin/Roles.vue')
          },
          {
            path: 'role-management',
            name: 'role-management',
            component: () => import('@/views/admin/RoleManagement.vue')
          },
          {
            path: 'audit',
            name: 'audit-logs',
            component: () => import('@/views/admin/AuditLogs.vue')
          },
          {
            path: 'financial-audit',
            name: 'financial-audit',
            component: () => import('@/views/admin/FinancialAudit.vue')
          },
          {
            path: 'settings',
            name: 'system-settings',
            component: () => import('@/views/admin/SystemSettings.vue')
          }
        ]
      }

    ]
  },

  // ================= SYSTEM =================
  {
    path: '/access-denied',
    name: 'access-denied',
    component: () => import('@/views/system/AccessDenied.vue')
  },
  {
    path: '/maintenance',
    name: 'maintenance',
    component: () => import('@/views/system/Maintenance.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notfound',
    component: () => import('@/views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// ================= NAVIGATION GUARD =================
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  const userRole = localStorage.getItem('role');

  if (to.meta.public) {
    if (isAuthenticated && to.name === 'login') {
      next('/app/dashboard');
    } else {
      next();
    }
    return;
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
    return;
  }

  if (to.meta.roles && !to.meta.roles.includes(userRole)) {
    next('/access-denied');
    return;
  }

  next();
});

export default router;