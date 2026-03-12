<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <h5>AI Assistant</h5>
        <div class="surface-100 p-4 border-round mb-3" style="min-height: 400px">
          <div v-for="(msg, i) in messages" :key="i" class="mb-3">
            <div :class="msg.role === 'user' ? 'text-right' : 'text-left'">
              <span class="inline-block p-3 border-round" 
                    :class="msg.role === 'user' ? 'bg-blue-500 text-white' : 'surface-card'">
                {{ msg.content }}
              </span>
            </div>
          </div>
        </div>
        <div class="flex gap-2">
          <InputText v-model="userInput" placeholder="Ask me anything..." class="flex-1" @keyup.enter="sendMessage" />
          <Button label="Send" icon="pi pi-send" @click="sendMessage" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

const messages = ref([
  { role: 'assistant', content: 'Hello! How can I help with your construction project today?' }
]);

const userInput = ref('');

const sendMessage = () => {
  if (userInput.value.trim()) {
    messages.value.push({ role: 'user', content: userInput.value });
    userInput.value = '';
    // TODO: Send to AI API
    setTimeout(() => {
      messages.value.push({ role: 'assistant', content: 'I received your message. AI response will be here.' });
    }, 1000);
  }
};
</script>