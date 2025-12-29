<template>
  <div id="app">
    <AppHeader v-if="showLayout" />
    <div class="app-body">
      <AppSidebar v-if="showLayout" />
      <main class="app-content">
        <router-view />   <!-- MUST ALWAYS BE HERE -->
      </main>
    </div>
  </div>
</template>


<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

import AppHeader from "@/components/layout/AppHeader.vue";
import AppSidebar from "@/components/layout/AppSidebar.vue";

const route = useRoute();

/**
 * Show layout on all pages EXCEPT auth pages
 */
const showLayout = computed(() => {
  return !route.path.startsWith("/login");
});
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-body {
  display: flex;
  flex: 1;
}

.app-content {
  flex: 1;
  padding: 24px;
  background: #f4f6f8;
}
</style>
