<template>
  <div class="min-h-screen flex align-items-center justify-content-center">
    <div class="text-center">
      <h1 class="text-6xl font-bold text-red-500">403</h1>
      <h2 class="text-2xl mb-4">Access Denied</h2>
      <p class="text-600 mb-4">You don't have permission to access this page.</p>
      <router-link to="/app/dashboard">
        <Button label="Go to Dashboard" icon="pi pi-home" />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button';
</script>
