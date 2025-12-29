<template>
  <aside class="sidebar">
    <nav class="nav">
      <h4 class="section">Main</h4>
      <router-link to="/dashboard" class="link">Dashboard</router-link>

      <h4 class="section">Modules</h4>
      <router-link to="/projects" class="link">Projects</router-link>
      <router-link to="/progress" class="link">Progress</router-link>
      <router-link to="/finance" class="link">Finance</router-link>
      <router-link to="/qa" class="link">QA / QC</router-link>
      <router-link to="/notifications" class="link">Notifications</router-link>
      <router-link to="/ai" class="link">AI Assistant</router-link>

      <h4 class="section">Account</h4>
      <router-link to="/account/profile" class="link">Profile</router-link>
      <router-link to="/account/security" class="link">Security</router-link>
      <router-link to="/account/preferences" class="link">Preferences</router-link>
    </nav>
  </aside>
</template>

<script setup>
// UI only – no logic yet
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 20px;
  overflow-y: auto;
}

.nav {
  display: flex;
  flex-direction: column;
}

.section {
  margin-top: 20px;
  margin-bottom: 8px;
  font-size: 13px;
  text-transform: uppercase;
  color: #6b7280;
}

.link {
  padding: 8px 10px;
  border-radius: 6px;
  color: #374151;
  text-decoration: none;
  margin-bottom: 4px;
}

.link:hover {
  background: #f3f4f6;
}

.router-link-active {
  background: #e5e7eb;
  font-weight: 600;
}
</style>
