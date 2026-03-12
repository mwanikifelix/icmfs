<template>
  <div class="min-h-screen flex align-items-center justify-content-center surface-ground">
    <div class="surface-card p-4 shadow-2 border-round w-full lg:w-4">
      <div class="text-center mb-5">
        <div class="text-900 text-3xl font-medium mb-3">Password Recovery</div>
      </div>
      <div>
        <label class="block text-900 font-medium mb-2">Email</label>
        <InputText type="text" placeholder="Enter your email" class="w-full mb-3" />
        <Button label="Reset Password" class="w-full" />
      </div>
    </div>
  </div>
</template>

<script setup>
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
</script>
