<template>
  <div class="dashboard">
    <h1 class="title">Dashboard</h1>
    <p class="subtitle">
      Welcome to the Integrated Multi-Site Construction Management System
    </p>

    <div class="grid">
      <div class="card">
        <h3>Projects</h3>
        <p>Manage construction projects and timelines.</p>
      </div>

      <div class="card">
        <h3>Progress</h3>
        <p>Track daily work, milestones, and reports.</p>
      </div>

      <div class="card">
        <h3>Finance</h3>
        <p>Monitor budgets, expenses, and payments.</p>
      </div>

      <div class="card">
        <h3>QA / QC</h3>
        <p>Quality assurance, inspections, and reports.</p>
      </div>

      <div class="card">
        <h3>Notifications</h3>
        <p>System alerts and important updates.</p>
      </div>

      <div class="card">
        <h3>AI Assistant</h3>
        <p>Insights, predictions, and smart analysis.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// UI-only dashboard (safe)
// No auth, no API, no side effects
</script>

<style scoped>
.dashboard {
  padding: 24px;
}

.title {
  font-size: 28px;
  margin-bottom: 6px;
}

.subtitle {
  color: #666;
  margin-bottom: 24px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.card {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.card h3 {
  margin-bottom: 8px;
}
</style>
