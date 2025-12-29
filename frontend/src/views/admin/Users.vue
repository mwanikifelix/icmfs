<!-- <script setup>
import { ref, onMounted } from "vue";
import { fetchUsers, createUser, toggleUserStatus } from "@/api/users";
import { fetchRoles } from "@/api/roles";

const users = ref([]);
const roles = ref([]);

const form = ref({
  username: "",
  password: "",
  role: "",
});

async function load() {
  users.value = (await fetchUsers()).data;
  roles.value = (await fetchRoles()).data;
}

async function submit() {
  await createUser(form.value);
  form.value = { username: "", password: "", role: "" };
  await load();
}

async function toggle(id) {
  await toggleUserStatus(id);
  await load();
}

onMounted(load);
</script>

<template>
  <div>
    <h2>Users</h2>

    <form @submit.prevent="submit">
      <input v-model="form.username" placeholder="Username" required />
      <input v-model="form.password" type="password" placeholder="Password" required />

      <select v-model="form.role" required>
        <option disabled value="">Select Role</option>
        <option v-for="r in roles" :key="r.id" :value="r.id">
          {{ r.name }}
        </option>
      </select>

      <button>Create User</button>
    </form>

    <hr />

    <table border="1" cellpadding="6">
      <tr>
        <th>Username</th>
        <th>Role</th>
        <th>Status</th>
        <th>Action</th>
      </tr>

      <tr v-for="u in users" :key="u.id">
        <td>{{ u.username }}</td>
        <td>{{ u.role?.name }}</td>
        <td>{{ u.is_active ? "Active" : "Disabled" }}</td>
        <td>
          <button @click="toggle(u.id)">
            {{ u.is_active ? "Disable" : "Enable" }}
          </button>
        </td>
      </tr>
    </table>
  </div>
</template>
 -->
<script setup>
import { onMounted, ref } from "vue";
import api from "@/services/api";

const users = ref([]);

onMounted(async () => {
  const res = await api.get("/admin_panel/users/");
  users.value = res.data;
});
</script>

<template>
  <div>
    <h2>Admin Users</h2>

    <ul>
      <li v-for="u in users" :key="u.id">
        {{ u.username }} — {{ u.role }}
      </li>
    </ul>
  </div>
</template>

