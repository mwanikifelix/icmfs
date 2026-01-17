<template>
  <div class="min-h-screen flex align-items-center justify-content-center surface-ground">
    <div class="surface-card p-4 shadow-2 border-round w-full lg:w-4">
      <div class="text-center mb-5">
        <div class="text-900 text-3xl font-medium mb-3">Login</div>
      </div>
      <div>
        <label for="email" class="block text-900 font-medium mb-2">Email</label>
        <InputText id="email" v-model="email" type="text" placeholder="Email" class="w-full mb-3" />
        
        <label for="password" class="block text-900 font-medium mb-2">Password</label>
        <Password id="password" v-model="password" placeholder="Password" :feedback="false" toggleMask class="w-full mb-3" />
        
        <Button label="Sign In" icon="pi pi-user" class="w-full" @click="login" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';

const router = useRouter();
const email = ref('');
const password = ref('');

const login = () => {
  localStorage.setItem('token', 'mock-token');
  localStorage.setItem('role', 'admin');
  router.push('/app/dashboard');
};
</script>
