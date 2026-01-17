<template>
  <div class="min-h-screen flex align-items-center justify-content-center surface-ground">
    <div class="surface-card p-4 shadow-2 border-round w-full lg:w-4">
      <div class="text-center mb-5">
        <div class="text-900 text-3xl font-medium mb-3">Register</div>
      </div>
      <div>
        <InputText type="text" placeholder="Full Name" class="w-full mb-3" />
        <InputText type="text" placeholder="Email" class="w-full mb-3" />
        <Password placeholder="Password" :feedback="true" toggleMask class="w-full mb-3" />
        <Button label="Create Account" icon="pi pi-user-plus" class="w-full" />
      </div>
    </div>
  </div>
</template>

<script setup>
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
</script>
