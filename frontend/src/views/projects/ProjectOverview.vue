<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <h5>{{ project.name }}</h5>
        <div class="grid">
          <div class="col-12 md:col-3">
            <div class="text-500 font-medium mb-2">Client</div>
            <div class="text-900">{{ project.client }}</div>
          </div>
          <div class="col-12 md:col-3">
            <div class="text-500 font-medium mb-2">Status</div>
            <Badge :value="project.status" severity="success" />
          </div>
          <div class="col-12 md:col-3">
            <div class="text-500 font-medium mb-2">Progress</div>
            <ProgressBar :value="project.progress" :showValue="true" />
          </div>
          <div class="col-12 md:col-3">
            <div class="text-500 font-medium mb-2">Budget</div>
            <div class="text-900 font-semibold">{{ project.budget }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-12 md:col-6">
      <div class="card">
        <h6>Project Details</h6>
        <p>{{ project.description }}</p>
      </div>
    </div>
    <div class="col-12 md:col-6">
      <div class="card">
        <h6>Key Metrics</h6>
        <p>Project metrics and KPIs will be displayed here</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Badge from 'primevue/badge';
import ProgressBar from 'primevue/progressbar';

const project = ref({
  name: 'Office Complex A',
  client: 'ABC Corporation',
  status: 'Active',
  progress: 65,
  budget: '$2.5M',
  description: 'Modern office complex with 10 floors and parking facilities.'
});
</script>