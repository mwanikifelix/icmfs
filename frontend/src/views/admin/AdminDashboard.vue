<!-- <script setup>
import { ref, onMounted } from "vue";
import { getAdminStats } from "@/services/adminAnalytics";

const stats = ref(null);
const loading = ref(true);

onMounted(async () => {
  try {
    stats.value = await getAdminStats();
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <h1>Admin Dashboard</h1>

    <p v-if="loading">Loading analytics…</p>

    <div v-else class="grid">
      <div class="card">Users: {{ stats.users }}</div>
      <div class="card">Projects: {{ stats.projects }}</div>
      <div class="card">Active Projects: {{ stats.activeProjects }}</div>
      <div class="card">Pending QA: {{ stats.pendingQA }}</div>
      <div class="card">Notifications: {{ stats.notifications }}</div>
      <div class="card">Audit Logs: {{ stats.auditLogs }}</div>
    </div>

    <hr />

    <nav>
      <RouterLink to="/admin/users">Manage Users</RouterLink> |
      <RouterLink to="/admin/roles">Roles</RouterLink> |
      <RouterLink to="/admin/permissions">Permissions</RouterLink> |
      <RouterLink to="/admin/audit-logs">Audit Logs</RouterLink>
    </nav>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.card {
  padding: 1rem;
  background: #8f6f6f;
  border-radius: 6px;
  font-weight: bold;
}
</style>
 -->

 <script setup>
import { onMounted, ref } from "vue";
import { fetchAdminAnalytics } from "@/api/adminAnalytics";
import KpiCard from "@/components/admin/KpiCard.vue";
import UserStatsChart from "@/components/admin/UserStatsChart.vue";

const analytics = ref(null);

onMounted(async () => {
  const res = await fetchAdminAnalytics();
  analytics.value = res.data;
});
</script>

<template>
  <div v-if="analytics">
    <h1>Admin Analytics</h1>

    <div class="grid">
      <KpiCard title="Total Users" :value="analytics.users.total" />
      <KpiCard title="Active Users" :value="analytics.users.active" />
      <KpiCard title="Staff" :value="analytics.users.staff" />
      <KpiCard title="Admins" :value="analytics.users.admins" />
      <KpiCard title="Audit Logs" :value="analytics.audit_logs.total" />
    </div>

    <UserStatsChart :stats="analytics.users" />
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
</style>
