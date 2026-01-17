<template>
  <div class="card">
    <h2>API Connection Test</h2>
    <Button label="Test Backend" @click="testConnection" />
    <p v-if="result">{{ result }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/service/api';
import Button from 'primevue/button';

const result = ref('');

const testConnection = async () => {
  try {
    const response = await api.get('/'); // Adjust endpoint as needed
    result.value = 'Connected! ' + JSON.stringify(response.data);
  } catch (error) {
    result.value = 'Error: ' + error.message;
  }
};
</script>