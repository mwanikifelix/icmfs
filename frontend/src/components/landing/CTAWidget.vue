<template>
  <section class="py-8">
    <div class="max-w-screen-xl mx-auto px-4">
      <div class="surface-card p-6 border-round shadow-2 text-center">
        <h2 class="text-4xl font-bold text-900 mb-3">Ready to Get Started?</h2>
        <p class="text-xl text-600 mb-5">Join thousands of users managing construction projects efficiently</p>
        <router-link to="/register">
          <Button label="Create Account" icon="pi pi-user-plus" size="large" class="mr-3" />
        </router-link>
        <router-link to="/contact">
          <Button label="Contact Support" severity="secondary" outlined size="large" />
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import Button from 'primevue/button'
</script>