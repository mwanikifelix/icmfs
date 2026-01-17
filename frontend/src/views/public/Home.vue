<template>
  <div class="min-h-screen flex align-items-center justify-content-center surface-ground">
    <div class="text-center">
      <h1 class="text-6xl font-bold mb-4 text-primary">ICMFS</h1>
      <p class="text-xl text-600 mb-4">Integrated Construction Management & Financing System</p>
      <router-link to="/login">
        <Button label="Get Started" icon="pi pi-arrow-right" iconPos="right" size="large" />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button';
</script>
