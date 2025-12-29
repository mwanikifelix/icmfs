<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";

const logs = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await api.get("/admin_panel/audit-logs/");
    logs.value = res.data;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <h2>Audit Logs</h2>

    <p v-if="loading">Loading...</p>

    <table v-else border="1" width="100%">
      <thead>
        <tr>
          <th>User</th>
          <th>Action</th>
          <th>Resource</th>
          <th>Metadata</th>
          <th>Date</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="log in logs" :key="log.id">
          <td>{{ log.user }}</td>
          <td>{{ log.action }}</td>
          <td>{{ log.resource }}</td>
          <td>{{ log.metadata }}</td>
          <td>{{ new Date(log.created_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
