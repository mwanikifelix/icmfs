<template>
  <ul class="layout-menu">
    <template v-for="(item, i) in model" :key="item.label || i">
      <li v-if="!item.separator" class="layout-menuitem">
        <router-link v-if="item.to" :to="item.to" class="p-ripple" :class="{ 'active-route': isActiveRoute(item) }">
          <i :class="item.icon" class="layout-menuitem-icon"></i>
          <span class="layout-menuitem-text">{{ item.label }}</span>
        </router-link>
        
        <a v-if="!item.to" :href="item.url" :target="item.target" class="p-ripple">
          <i :class="item.icon" class="layout-menuitem-icon"></i>
          <span class="layout-menuitem-text">{{ item.label }}</span>
          <i v-if="item.items" class="pi pi-fw pi-angle-down layout-submenu-toggler"></i>
        </a>

        <ul v-if="item.items" class="layout-submenu">
          <li v-for="(child, j) in item.items" :key="j" class="layout-menuitem">
            <router-link :to="child.to" class="p-ripple" :class="{ 'active-route': isActiveRoute(child) }">
              <i :class="child.icon" class="layout-menuitem-icon"></i>
              <span class="layout-menuitem-text">{{ child.label }}</span>
            </router-link>
          </li>
        </ul>
      </li>
      <li v-else class="menu-separator"></li>
    </template>
  </ul>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const model = ref([
  {
    label: 'Dashboard',
    icon: 'pi pi-fw pi-home',
    to: '/app/dashboard'
  },
  {
    label: 'Projects',
    icon: 'pi pi-fw pi-building',
    items: [
      { label: 'All Projects', icon: 'pi pi-fw pi-list', to: '/app/projects' },
      { label: 'Create Project', icon: 'pi pi-fw pi-plus', to: '/app/projects/create' }
    ]
  },
  {
    label: 'Progress',
    icon: 'pi pi-fw pi-chart-line',
    items: [
      { label: 'Overview', icon: 'pi pi-fw pi-eye', to: '/app/progress/overview' },
      { label: 'Daily Reports', icon: 'pi pi-fw pi-file-edit', to: '/app/progress/reports' },
      { label: 'EVM Analysis', icon: 'pi pi-fw pi-chart-bar', to: '/app/progress/evm' }
    ]
  },
  {
    label: 'Finance',
    icon: 'pi pi-fw pi-dollar',
    items: [
      { label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/app/finance/dashboard' },
      { label: 'Expenses', icon: 'pi pi-fw pi-wallet', to: '/app/finance/expenses' },
      { label: 'Payments', icon: 'pi pi-fw pi-credit-card', to: '/app/finance/payments' }
    ]
  },
  {
    label: 'QA',
    icon: 'pi pi-fw pi-verified',
    items: [
      { label: 'Issues', icon: 'pi pi-fw pi-exclamation-triangle', to: '/app/qa/issues' },
      { label: 'Inspections', icon: 'pi pi-fw pi-search', to: '/app/qa/inspection' }
    ]
  },
  {
    label: 'AI Insights',
    icon: 'pi pi-fw pi-sparkles',
    items: [
      { label: 'Assistant', icon: 'pi pi-fw pi-comments', to: '/app/ai/assistant' },
      { label: 'Insights', icon: 'pi pi-fw pi-chart-scatter', to: '/app/ai/insights' }
    ]
  },
  { separator: true },
  {
    label: 'Account',
    icon: 'pi pi-fw pi-user',
    to: '/app/profile'
  }
]);

const isActiveRoute = (item) => {
  return route.path === item.to;
};
</script>
