<script setup>
import { ref, onMounted } from "vue";
import {
  fetchRoles,
  createRole,
  updateRole,
  fetchPermissions,
} from "@/services/adminRoles";

const roles = ref([]);
const permissions = ref([]);
const selectedRole = ref(null);
const roleName = ref("");
const rolePermissions = ref([]);

onMounted(async () => {
  const [r, p] = await Promise.all([
    fetchRoles(),
    fetchPermissions(),
  ]);

  roles.value = r.data;
  permissions.value = p.data;
});

function editRole(role) {
  selectedRole.value = role;
  roleName.value = role.name;
  rolePermissions.value = [...role.permissions];
}

async function saveRole() {
  const payload = {
    name: roleName.value,
    permissions: rolePermissions.value,
  };

  if (selectedRole.value) {
    await updateRole(selectedRole.value.id, payload);
  } else {
    await createRole(payload);
  }

  location.reload(); // simple + safe
}
</script>

<template>
  <div>
    <h2>Roles Management</h2>

    <div style="display:flex; gap:2rem;">
      <!-- Role List -->
      <div>
        <h3>Existing Roles</h3>
        <ul>
          <li
            v-for="role in roles"
            :key="role.id"
            @click="editRole(role)"
            style="cursor:pointer;"
          >
            {{ role.name }}
          </li>
        </ul>
      </div>

      <!-- Editor -->
      <div>
        <h3>{{ selectedRole ? "Edit Role" : "Create Role" }}</h3>

        <input
          v-model="roleName"
          placeholder="Role name"
        />

        <h4>Permissions</h4>
        <div v-for="perm in permissions" :key="perm.id">
          <label>
            <input
              type="checkbox"
              :value="perm.code"
              v-model="rolePermissions"
            />
            {{ perm.name }}
          </label>
        </div>

        <br />
        <button @click="saveRole">
          Save Role
        </button>
      </div>
    </div>
  </div>
</template>
