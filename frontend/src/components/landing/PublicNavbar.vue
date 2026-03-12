<template>
  <nav class="surface-card shadow-2 px-4 py-3">
    <div class="flex justify-content-between align-items-center max-w-screen-xl mx-auto">
      <div class="flex align-items-center gap-2">
        <i class="pi pi-building text-primary text-3xl"></i>
        <span class="text-2xl font-bold text-900">ICMFS</span>
      </div>
      <div class="flex gap-4 align-items-center">
        <router-link to="/" class="text-700 hover:text-primary no-underline">Home</router-link>
        <router-link to="/about" class="text-700 hover:text-primary no-underline">About</router-link>
        <router-link to="/contact" class="text-700 hover:text-primary no-underline">Contact</router-link>
        <router-link to="/login">
          <Button label="Login" outlined class="mr-2" />
        </router-link>
        <router-link to="/register">
          <Button label="Register" />
        </router-link>
      </div> 
    </div>
  </nav>
</template>

<script setup>
import Button from 'primevue/button' 
</script>