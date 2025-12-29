<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

const submit = async () => {
  error.value = "";

  try {
    await auth.login({
      username: username.value,
      password: password.value,
    });

    router.replace("/dashboard");
  } catch (err) {
    error.value = "Invalid username or password";
  }
};

</script>

<template>
  <div class="login-container">
    <h1>Login</h1>

    <form @submit.prevent="submit">
      <input
        v-model="username"
        placeholder="Username"
        autocomplete="username"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        autocomplete="current-password"
        required
      />

      <button type="submit" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 80px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

input {
  display: block;
  width: 100%;
  margin-bottom: 12px;
  padding: 10px;
}

button {
  width: 100%;
  padding: 10px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>

<!-- 
 <template>
  <div style="padding:40px">
    <h1>Login Page</h1>
  </div>
</template>

<script setup>
</script>
 -->