<!-- ============================================ -->
<!-- PATTERN 1: Standard Form Page Wrapper -->
<!-- src/components/common/PageWrapper.vue -->
<!-- ============================================ -->
<script setup>
defineProps({
  title: String,
  subtitle: String,
  showBreadcrumb: { type: Boolean, default: true },
  breadcrumbItems: Array
})
</script>

<template>
  <div class="page-wrapper">
    <!-- Breadcrumb -->
    <div v-if="showBreadcrumb" class="mb-4">
      <Breadcrumb :home="{ icon: 'pi pi-home', to: '/app/dashboard' }" :model="breadcrumbItems" />
    </div>

    <!-- Page Header -->
    <div class="page-header mb-4">
      <h1 class="text-3xl font-bold text-gray-800">{{ title }}</h1>
      <p v-if="subtitle" class="text-gray-600 mt-2">{{ subtitle }}</p>
    </div>

    <!-- Main Content Slot -->
    <div class="page-content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.page-wrapper {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 1rem;
}
</style>

