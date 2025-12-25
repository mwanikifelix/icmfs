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
    testBackend() {
      fetch("/api/accounts/health/")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Backend not reachable");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          this.backendStatus = "Backend reachable ✅";
        })
        .catch((error) => {
          console.error(error);
          this.backendStatus = "Backend not reachable ❌";
        });
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
