<template>
  <header class="header">
    <div class="left">
      <h2 class="logo">ICMFS</h2>
    </div>

    <div class="right">
      <span class="user" v-if="user">
        {{ user.username }}
      </span>

      <button class="logout" @click="handleLogout">
        Logout
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();

const user = computed(() => auth.user);

const handleLogout = async () => {
  auth.logout();

  await router.replace("/login");
};

</script>

<style scoped>
.header {
  height: 60px;
  background: #1e1e2f;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.logo {
  margin: 0;
}

.right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user {
  font-size: 14px;
  opacity: 0.9;
}

.logout {
  background: #ef4444;
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.logout:hover {
  background: #dc2626;
}
</style>
