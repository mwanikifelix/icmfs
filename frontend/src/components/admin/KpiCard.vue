<template>
  <div class="kpi-card">
    <h3>{{ title }}</h3>
    <p>{{ value }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
});
</script>

<style scoped>
.kpi-card {
  padding: 1rem;
  border-radius: 8px;
  background: #1e293b;
  color: white;
}
</style>
