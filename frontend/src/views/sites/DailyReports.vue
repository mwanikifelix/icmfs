<script setup>
import { ref } from "vue";

const report = ref({
  weather: "",
  progress: "",
  challenges: ""
});
</script>

<template>
  <div class="grid">
    <div class="col-4">
      <Dropdown v-model="report.weather"
        :options="['Sunny','Rainy','Cloudy']"
        placeholder="Weather" />
    </div>

    <div class="col-12">
      <Textarea v-model="report.progress" rows="3" placeholder="Work Progress" />
    </div>

    <div class="col-12">
      <Textarea v-model="report.challenges" rows="3" placeholder="Challenges" />
    </div>

    <Button label="Submit Report" />
  </div>
</template>
