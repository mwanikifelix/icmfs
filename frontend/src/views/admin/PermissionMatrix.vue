<script setup>
import { ref, onMounted } from "vue";
import {
  fetchRoles,
  fetchPermissions,
  updateRolePermissions,
} from "@/services/adminPermissions";

const roles = ref([]);
const permissions = ref([]);
const loading = ref(false);

onMounted(async () => {
  const [r, p] = await Promise.all([
    fetchRoles(),
    fetchPermissions(),
  ]);

  roles.value = r.data;
  permissions.value = p.data;
});

function hasPermission(role, permCode) {
  return role.permissions.includes(permCode);
}

async function togglePermission(role, permCode) {
  const updated = hasPermission(role, permCode)
    ? role.permissions.filter((p) => p !== permCode)
    : [...role.permissions, permCode];

  role.permissions = updated;

  loading.value = true;
  try {
    await updateRolePermissions(role.id, updated);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div>
    <h2>Permission Matrix</h2>

    <table border="1" cellpadding="8">
      <thead>
        <tr>
          <th>Permission</th>
          <th v-for="role in roles" :key="role.id">
            {{ role.name }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="perm in permissions" :key="perm.code">
          <td>{{ perm.name }}</td>

          <td v-for="role in roles" :key="role.id">
            <input
              type="checkbox"
              :checked="hasPermission(role, perm.code)"
              @change="togglePermission(role, perm.code)"
              :disabled="loading"
            />
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="loading">Saving changes…</p>
  </div>
</template>
