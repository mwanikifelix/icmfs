<script setup>
import { onMounted, ref } from "vue";
import { fetchPermissions } from "@/services/admin";
import AdminTable from "@/components/admin/AdminTable.vue";

const permissions = ref([]);
const columns = ["id", "codename", "name"];

onMounted(async () => {
  const res = await fetchPermissions();
  permissions.value = res.data;
});
</script>

<template>
  <div>
    <h2>Admin – Permissions</h2>
    <AdminTable :columns="columns" :rows="permissions" />
  </div>
</template>
