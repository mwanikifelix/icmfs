<template>
  <ul class="layout-menu">
    <template v-for="(item, i) in menuItems" :key="item.label || i">
      <li v-if="!item.separator" class="layout-menuitem" :class="{ 'active-menuitem': isMenuActive(i) }">

        <!-- Menu item with submenu -->
        <a
          v-if="item.items"
          @click="toggleMenu($event, i)"
          class="p-ripple"
          :class="{ 'active-route': isActiveRoute(item) }"
        >
          <i :class="item.icon" class="layout-menuitem-icon"></i>
          <span class="layout-menuitem-text">{{ item.label }}</span>
          <i class="pi pi-fw pi-angle-down layout-submenu-toggler"></i>
        </a>

        <!-- Menu item without submenu -->
        <router-link
          v-else-if="item.to"
          :to="item.to"
          class="p-ripple"
          :class="{ 'active-route': isActiveRoute(item) }"
        >
          <i :class="item.icon" class="layout-menuitem-icon"></i>
          <span class="layout-menuitem-text">{{ item.label }}</span>
        </router-link>

        <!-- Submenu items -->
        <transition name="layout-submenu">
          <ul v-if="item.items" v-show="isMenuActive(i)" class="layout-submenu">
            <li v-for="(child, j) in item.items" :key="j" class="layout-menuitem">
              <router-link
                :to="child.to"
                class="p-ripple"
                :class="{ 'active-route': isActiveRoute(child) }"
              >
                <i :class="child.icon" class="layout-menuitem-icon"></i>
                <span class="layout-menuitem-text">{{ child.label }}</span>
              </router-link>
            </li>
          </ul>
        </transition>
      </li>
      <li v-else class="menu-separator"></li>
    </template>
  </ul>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const activeMenus = ref([]);

const menuItems = ref([

  // ========== DASHBOARD ==========
  {
    label: 'Dashboard',
    icon: 'pi pi-fw pi-home',
    to: '/app/dashboard'
  },

  // ========== REGIONS ==========
  {
    label: 'Regions',
    icon: 'pi pi-fw pi-map',
    items: [
      { label: 'All Regions',     icon: 'pi pi-fw pi-globe',      to: '/app/regions'          },
      { label: 'Counties',        icon: 'pi pi-fw pi-map-marker', to: '/app/regions/counties' }
    ]
  },

  // ========== PROJECTS ==========
  {
    label: 'Projects',
    icon: 'pi pi-fw pi-building',
    items: [
      { label: 'All Projects',    icon: 'pi pi-fw pi-list', to: '/app/projects'        },
      { label: 'Create Project',  icon: 'pi pi-fw pi-plus', to: '/app/projects/create' },
      { label: 'Project Details',  icon: 'pi pi-fw pi-details', to: '/app/projects/details' }
    ]
  },

  // ========== SITES ==========
  {
    label: 'Sites',
    icon: 'pi pi-fw pi-map-marker',
    items: [
      { label: 'All Sites',       icon: 'pi pi-fw pi-list',      to: '/app/sites'               },
      { label: 'Create Site',     icon: 'pi pi-fw pi-plus',      to: '/app/sites/create'        },
      { label: 'Daily Reports',   icon: 'pi pi-fw pi-file-edit', to: '/app/sites/daily-reports' },
      { label: 'Workforce',       icon: 'pi pi-fw pi-users',     to: '/app/sites/workforce'     }
    ]
  },

  // ========== PROGRESS & EVM ==========
  {
    label: 'Progress & EVM',
    icon: 'pi pi-fw pi-chart-line',
    items: [
      { label: 'Progress Overview',  icon: 'pi pi-fw pi-eye',       to: '/app/progress/overview'      },
      { label: 'Daily Logs',         icon: 'pi pi-fw pi-file-edit', to: '/app/progress/daily-logs'    },
      { label: 'Daily Reports',      icon: 'pi pi-fw pi-file',      to: '/app/progress/daily-reports' },
      { label: 'EVM Analysis',       icon: 'pi pi-fw pi-chart-bar', to: '/app/progress/evm'           },
      { label: 'Performance Trends', icon: 'pi pi-fw pi-arrow-up',  to: '/app/progress/trends'        }
    ]
  },

  // ========== FINANCE ==========
  {
    label: 'Finance',
    icon: 'pi pi-fw pi-dollar',
    items: [
      { label: 'Finance Dashboard', icon: 'pi pi-fw pi-home',      to: '/app/finance/dashboard' },
      { label: 'Expenses',          icon: 'pi pi-fw pi-wallet',    to: '/app/finance/expenses'  },
      { label: 'Budget Tracking',   icon: 'pi pi-fw pi-chart-pie', to: '/app/finance/budget'    },
      { label: 'Financial Reports', icon: 'pi pi-fw pi-file-pdf',  to: '/app/finance/reports'   }
    ]
  },

  // ========== PAYMENTS ==========
  {
    label: 'Payments & Disbursement',
    icon: 'pi pi-fw pi-credit-card',
    items: [
      { label: 'Payments Dashboard',  icon: 'pi pi-fw pi-home',         to: '/app/payments/dashboard'         },
      { label: 'Payment Approvals',   icon: 'pi pi-fw pi-check',        to: '/app/payments/approvals'         },
      { label: 'M-Pesa Payments',     icon: 'pi pi-fw pi-mobile',       to: '/app/payments/mpesa'             },
      { label: 'Bank Payments',       icon: 'pi pi-fw pi-building',     to: '/app/payments/bank'              },
      { label: 'M-Pesa Transactions', icon: 'pi pi-fw pi-list',         to: '/app/payments/mpesa-transactions'},
      { label: 'Payment Audit',       icon: 'pi pi-fw pi-eye',          to: '/app/payments/audit'             },
      { label: 'Reconciliation',      icon: 'pi pi-fw pi-check-square', to: '/app/payments/reconciliation'    }
    ]
  },

  // ========== SUPPLIERS ==========
  {
    label: 'Suppliers',
    icon: 'pi pi-fw pi-truck',
    items: [
      { label: 'All Suppliers',     icon: 'pi pi-fw pi-list',          to: '/app/suppliers'           },
      { label: 'Purchase Orders',   icon: 'pi pi-fw pi-shopping-cart', to: '/app/suppliers/orders'    },
      { label: 'Deliveries',        icon: 'pi pi-fw pi-map-marker',    to: '/app/suppliers/deliveries'},
      { label: 'Supplier Invoices', icon: 'pi pi-fw pi-file',          to: '/app/suppliers/invoices'  },
      { label: 'Supplier Payments', icon: 'pi pi-fw pi-wallet',        to: '/app/suppliers/payments'  }
    ]
  },

  // ========== PROCUREMENT ==========
  {
    label: 'Procurement',
    icon: 'pi pi-fw pi-shopping-bag',
    items: [
      { label: 'Procurement Dashboard', icon: 'pi pi-fw pi-home',         to: '/app/procurement/dashboard'          },
      { label: 'Purchase Requests',     icon: 'pi pi-fw pi-file',         to: '/app/procurement/requests'           },
      { label: 'Supplier Management',   icon: 'pi pi-fw pi-users',        to: '/app/procurement/supplier-management'},
      { label: 'Inventory',             icon: 'pi pi-fw pi-box',          to: '/app/procurement/inventory'          }
    ]
  },

  // ========== QUALITY ASSURANCE ==========
  {
    label: 'Quality Assurance',
    icon: 'pi pi-fw pi-verified',
    items: [
      { label: 'QA Overview',    icon: 'pi pi-fw pi-list',               to: '/app/qa'                },
      { label: 'QA Issues',      icon: 'pi pi-fw pi-exclamation-circle', to: '/app/qa/issues'         },
      { label: 'Inspections',    icon: 'pi pi-fw pi-search',             to: '/app/qa/inspections'    },
      { label: 'Certification',  icon: 'pi pi-fw pi-check-circle',       to: '/app/qa/certification'  },
      { label: 'QA Reports',     icon: 'pi pi-fw pi-file-pdf',           to: '/app/qa/reports'        }
    ]
  },

  // ========== SAFETY & HEALTH ==========
  {
    label: 'Safety & Health',
    icon: 'pi pi-fw pi-shield',
    items: [
      { label: 'Safety Dashboard',  icon: 'pi pi-fw pi-home',               to: '/app/safety/dashboard'   },
      { label: 'Incident Reports',  icon: 'pi pi-fw pi-exclamation-triangle',to: '/app/safety/incidents'   },
      { label: 'Risk Assessments',  icon: 'pi pi-fw pi-chart-bar',          to: '/app/safety/assessments' },
      { label: 'Safety Audits',     icon: 'pi pi-fw pi-check',              to: '/app/safety/audits'      }
    ]
  },

  // ========== AI & ANALYTICS ==========
  {
    label: 'AI & Analytics',
    icon: 'pi pi-fw pi-sparkles',
    items: [
      { label: 'AI Assistant',     icon: 'pi pi-fw pi-comments',       to: '/app/ai/assistant' },
      { label: 'AI Insights',      icon: 'pi pi-fw pi-chart-scatter',  to: '/app/ai/insights'  },
      { label: 'Finance AI',       icon: 'pi pi-fw pi-dollar',         to: '/app/ai/finance'   },
      { label: 'Risk Predictions', icon: 'pi pi-fw pi-shield',         to: '/app/ai/risks'     }
    ]
  },

  // ========== NOTIFICATIONS ==========
  {
    label: 'Notifications',
    icon: 'pi pi-fw pi-bell',
    items: [
      { label: 'All Notifications', icon: 'pi pi-fw pi-list', to: '/app/notifications/list'  },
      { label: 'Settings',          icon: 'pi pi-fw pi-cog',  to: '/app/notifications/settings' }
    ]
  },

  // ========== TASKS ==========
  {
    label: 'Tasks',
    icon: 'pi pi-fw pi-check-square',
    to: '/app/tasks'
  },

  { separator: true },

  // ========== MY ACCOUNT ==========
  {
    label: 'My Account',
    icon: 'pi pi-fw pi-user',
    items: [
      { label: 'Profile',      icon: 'pi pi-fw pi-user-edit',  to: '/app/account/profile'      },
      { label: 'Security',     icon: 'pi pi-fw pi-lock',       to: '/app/account/security'     },
      { label: 'Preferences',  icon: 'pi pi-fw pi-sliders-h',  to: '/app/account/preferences'  }
    ]
  },

  // ========== ADMINISTRATION ==========
  {
    label: 'Administration',
    icon: 'pi pi-fw pi-cog',
    items: [
      { label: 'Admin Dashboard',  icon: 'pi pi-fw pi-home',    to: '/app/admin/dashboard'       },
      { label: 'User Management',  icon: 'pi pi-fw pi-users',   to: '/app/admin/users'           },
      { label: 'Role Management',  icon: 'pi pi-fw pi-key',     to: '/app/admin/roles'           },
      { label: 'Audit Logs',       icon: 'pi pi-fw pi-history', to: '/app/admin/audit'           },
      { label: 'Financial Audit',  icon: 'pi pi-fw pi-dollar',  to: '/app/admin/financial-audit' },
      { label: 'System Settings',  icon: 'pi pi-fw pi-cog',     to: '/app/admin/settings'        }
    ]
  },

  { separator: true },

  // ========== SYSTEM PAGES (Testing) ==========
  {
    label: 'System Pages',
    icon: 'pi pi-fw pi-info-circle',
    items: [
      { label: 'Access Denied', icon: 'pi pi-fw pi-ban',         to: '/access-denied' },
      { label: 'Maintenance',   icon: 'pi pi-fw pi-wrench',      to: '/maintenance'   },
      { label: '404 Not Found', icon: 'pi pi-fw pi-times-circle', to: '/nonexistent'  }
    ]
  }

]);

const toggleMenu = (event, index) => {
  event.preventDefault();
  const menuIndex = activeMenus.value.indexOf(index);
  if (menuIndex === -1) {
    activeMenus.value.push(index);
  } else {
    activeMenus.value.splice(menuIndex, 1);
  }
};

const isMenuActive  = (index) => activeMenus.value.includes(index);
const isActiveRoute = (item)  => route.path === item.to;
</script>

<style scoped>
.layout-menuitem > a {
  padding: 0.85rem 1.4rem;
  min-height: 44px;
  display: flex;
  align-items: center;
  border-radius: 10px;
}

.layout-submenu .layout-menuitem > a {
  padding: 0.75rem 1.6rem;
}

.layout-menuitem + .layout-menuitem {
  margin-top: 0.3rem;
}

.layout-menuitem-icon {
  margin-right: 0.85rem;
  font-size: 1.05rem;
}
</style>