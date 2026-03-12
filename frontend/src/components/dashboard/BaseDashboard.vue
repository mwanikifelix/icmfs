<!-- <script setup>
import { ref, computed, onMounted } from 'vue'
import { dashboardConfig } from '@/config/dashboardConfig'
import Card from 'primevue/card'
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'
import Chart from 'primevue/chart'

const props = defineProps({
  role: {
    type: String,
    required: true
  }
})

// Get configuration for this role
const config = computed(() => dashboardConfig[props.role] || dashboardConfig.default)

const userName = ref(localStorage.getItem('userName') || 'User')

// Sample stats data
const statsData = ref({
  stat1: { label: 'Active Projects', value: 45, icon: 'pi pi-building', color: 'bg-blue-100 text-blue-600' },
  stat2: { label: 'Active Sites', value: 28, icon: 'pi pi-map-marker', color: 'bg-green-100 text-green-600' },
  stat3: { label: 'Budget (KSH)', value: '2.4B', icon: 'pi pi-dollar', color: 'bg-purple-100 text-purple-600' },
  stat4: { label: 'Completion', value: '67%', icon: 'pi pi-chart-line', color: 'bg-orange-100 text-orange-600' }
})

// Sample projects data
const projects = ref([
  {
    id: 1,
    name: 'Nairobi Affordable Housing Phase 2',
    region: 'Nairobi',
    progress: 78,
    status: 'On Track',
    budget: 450000000
  },
  {
    id: 2,
    name: 'Mombasa County Housing Project',
    region: 'Coast',
    progress: 45,
    status: 'Delayed',
    budget: 320000000
  },
  {
    id: 3,
    name: 'Kisumu Lakeside Residences',
    region: 'Nyanza',
    progress: 92,
    status: 'On Track',
    budget: 280000000
  }
])

// Quick actions based on role
const quickActions = computed(() => {
  const actions = {
    project_manager: [
      { label: 'Create Project', icon: 'pi pi-plus', route: '/app/projects/create' },
      { label: 'Daily Report', icon: 'pi pi-file', route: '/app/sites/daily-reports' },
      { label: 'View Sites', icon: 'pi pi-map', route: '/app/sites' }
    ],
    finance_officer: [
      { label: 'Process Payment', icon: 'pi pi-money-bill', route: '/app/payments/mpesa' },
      { label: 'Budget Tracking', icon: 'pi pi-chart-bar', route: '/app/finance/budget' },
      { label: 'Approve Expenses', icon: 'pi pi-check-circle', route: '/app/finance/expenses' }
    ],
    safety_officer: [
      { label: 'Report Incident', icon: 'pi pi-exclamation-triangle', route: '/app/safety/incidents' },
      { label: 'Safety Audit', icon: 'pi pi-shield', route: '/app/safety/audits' }
    ],
    default: [
      { label: 'View Projects', icon: 'pi pi-building', route: '/app/projects' },
      { label: 'Reports', icon: 'pi pi-file', route: '/app/progress/overview' }
    ]
  }
  return actions[props.role] || actions.default
})

// Notifications
const notifications = ref([
  {
    id: 1,
    title: 'Payment Approved',
    message: 'KSH 2.5M payment approved',
    time: '5 minutes ago',
    type: 'success',
    icon: 'pi pi-check-circle'
  },
  {
    id: 2,
    title: 'Safety Alert',
    message: 'Minor incident at Site 3',
    time: '1 hour ago',
    type: 'warning',
    icon: 'pi pi-exclamation-triangle'
  }
])

const getStatusColor = (status) => {
  return status === 'On Track' ? 'success' : 'warning'
}

const getNotifColor = (type) => {
  const colors = {
    success: 'text-green-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600'
  }
  return colors[type] || 'text-gray-600'
}

onMounted(() => {
  console.log(`Loading ${props.role} dashboard`)
})
</script>

<template>
  <div class="dashboard-container">
    <!-- Welcome Section --
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900">{{ config.title }}</h1>
      <p class="text-gray-600 mt-1">{{ config.subtitle }}</p>
    </div>

    !-- Dashboard Grid --
    <div class="grid grid-cols-12 gap-6">
      !-- Stats Overview --
      <div v-if="config.widgets.includes('stats')" class="col-span-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card v-for="(stat, key) in statsData" :key="key" class="cursor-pointer hover:shadow-lg transition-shadow">
            <template #content>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-gray-600 text-sm mb-1">{{ stat.label }}</p>
                  <p class="text-2xl font-bold text-gray-900">{{ stat.value }}</p>
                </div>
                <div :class="stat.color" class="w-12 h-12 rounded-full flex items-center justify-center">
                  <i :class="stat.icon" class="text-2xl"></i>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </div>

      <!-- Left Column (8 cols) --
      <div class="col-span-12 xl:col-span-8">
        <div class="space-y-6">
          <!-- Recent Projects --
          <Card v-if="config.widgets.includes('projects')">
            <template #title>
              <div class="flex justify-between items-center">
                <h3 class="text-xl font-semibold">Recent Projects</h3>
                <router-link to="/app/projects">
                  <Button label="View All" text />
                </router-link>
              </div>
            </template>
            <template #content>
              <DataTable :value="projects" stripedRows>
                <Column field="name" header="Project Name"></Column>
                <Column field="region" header="Region"></Column>
                <Column field="progress" header="Progress">
                  <template #body="{ data }">
                    <ProgressBar :value="data.progress" :showValue="true" />
                  </template>
                </Column>
                <Column field="status" header="Status">
                  <template #body="{ data }">
                    <Tag :value="data.status" :severity="getStatusColor(data.status)" />
                  </template>
                </Column>
              </DataTable>
            </template>
          </Card>

          !-- Finance Overview --
          <Card v-if="config.widgets.includes('finance')">
            <template #title>
              <h3 class="text-xl font-semibold">Finance Overview</h3>
            </template>
            <template #content>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="text-center">
                  <p class="text-sm text-gray-600">Total Budget</p>
                  <p class="text-xl font-bold text-gray-900">2.45B</p>
                </div>
                <div class="text-center">
                  <p class="text-sm text-gray-600">Spent</p>
                  <p class="text-xl font-bold text-blue-600">1.65B</p>
                </div>
                <div class="text-center">
                  <p class="text-sm text-gray-600">Committed</p>
                  <p class="text-xl font-bold text-orange-600">450M</p>
                </div>
                <div class="text-center">
                  <p class="text-sm text-gray-600">Available</p>
                  <p class="text-xl font-bold text-green-600">350M</p>
                </div>
              </div>
            </template>
          </Card>

          !-- Safety Alerts --
          <Card v-if="config.widgets.includes('safety')">
            <template #title>
              <h3 class="text-xl font-semibold">Safety Alerts</h3>
            </template>
            <template #content>
              <div class="space-y-3">
                <div class="p-3 border rounded-lg">
                  <Tag value="HIGH" severity="danger" class="mb-2" />
                  <p class="font-semibold text-sm">PPE Compliance Issue</p>
                  <p class="text-xs text-gray-600">Nairobi Site 3 • 2026-02-02</p>
                </div>
                <div class="p-3 border rounded-lg">
                  <Tag value="MEDIUM" severity="warning" class="mb-2" />
                  <p class="font-semibold text-sm">Equipment Maintenance Due</p>
                  <p class="text-xs text-gray-600">Mombasa Site 1 • 2026-02-01</p>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </div>

      !-- Right Column (4 cols) --
      <div class="col-span-12 xl:col-span-4">
        <div class="space-y-6">
          !-- Quick Actions --
          <Card v-if="config.widgets.includes('quick-actions')">
            <template #title>
              <h3 class="text-xl font-semibold">Quick Actions</h3>
            </template>
            <template #content>
              <div class="space-y-3">
                <router-link 
                  v-for="action in quickActions" 
                  :key="action.label" 
                  :to="action.route"
                  class="no-underline block"
                >
                  <Button 
                    :label="action.label" 
                    :icon="action.icon"
                    class="w-full justify-start"
                  />
                </router-link>
              </div>
            </template>
          </Card>

          -- Notifications -
          <Card v-if="config.widgets.includes('notifications')">
            <template #title>
              <div class="flex justify-between items-center">
                <h3 class="text-xl font-semibold">Notifications</h3>
                <router-link to="/app/notifications">
                  <Button label="View All" text size="small" />
                </router-link>
              </div>
            </template>
            <template #content>
              <div class="space-y-4">
                <div 
                  v-for="notif in notifications" 
                  :key="notif.id"
                  class="flex items-start gap-3 pb-3 border-b last:border-0"
                >
                  <i :class="[notif.icon, getNotifColor(notif.type)]" class="text-xl mt-1"></i>
                  <div class="flex-1">
                    <p class="font-semibold text-sm text-gray-900">{{ notif.title }}</p>
                    <p class="text-sm text-gray-600">{{ notif.message }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ notif.time }}</p>
                  </div>
                </div>
              </div>
            </template>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 1.5rem;
}

.space-y-6 > * + * {
  margin-top: 1.5rem;
}

.space-y-3 > * + * {
  margin-top: 0.75rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}
</style> -->