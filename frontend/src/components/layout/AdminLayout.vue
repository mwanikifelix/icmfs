<template>
  <div class="admin-layout">
    <nav class="sidebar">
      <h3>Admin Panel</h3>

      <router-link to="/admin/dashboard">Dashboard</router-link>
      <router-link to="/admin/users">Users</router-link>
      <router-link to="/admin/roles">Roles</router-link>
    </nav>

    <main class="content">
      <router-view /> <!-- ✅ THIS RENDERS DASHBOARD -->
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: #1e1e2f;
  color: white;
  padding: 20px;
}

.sidebar a {
  display: block;
  color: white;
  margin: 10px 0;
  text-decoration: none;
}

.content {
  flex: 1;
  padding: 20px;
}
</style>
