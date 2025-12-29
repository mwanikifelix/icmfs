<template>
  <div class="home">
    <h1>Backend Test</h1>
    <p>{{ backendStatus }}</p>
    <button @click="testBackend">Test Backend</button>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      backendStatus: "Not tested yet",
    };
  },
  methods: {
      async testBackend() {
       try {
          const response = await fetch("/api/accounts/health/");

         if (!response.ok) {
           throw new Error(`HTTP ${response.status}`);
          }

         const data = await response.json();
         console.log("Backend response:", data);

         this.backendStatus = `Backend reachable ✅ (${data.status})`;
       } catch (error) {
         console.error("Backend error:", error);
          this.backendStatus = "Backend not reachable ❌";
       }
      },
    },
  };
</script>

<style scoped>
.home {
  padding: 20px;
}
button {
  margin-top: 10px;
}
</style>
