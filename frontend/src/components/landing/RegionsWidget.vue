
<template>
  <section class="py-8 surface-100">
    <div class="max-w-screen-xl mx-auto px-4">
      <div class="text-center mb-6">
        <h2 class="text-5xl font-bold text-900 mb-3">Nationwide Coverage</h2>
        <p class="text-xl text-600">Supporting Kenya's Affordable Housing across all regions</p>
      </div>
      <div class="grid">
        <div 
          v-for="region in regions" 
          :key="region.name" 
          class="col-12 md:col-4"
        >
          <div class="surface-card p-4 border-round text-center hover:shadow-4 transition-duration-200">
            <i class="pi pi-map-marker text-primary text-4xl mb-3"></i>
            <h4 class="text-xl font-semibold text-900 mb-2">{{ region.name }}</h4>
            <p class="text-600">{{ region.projects }} Projects</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const regions = ref([
  { name: 'Nairobi Region', projects: 45 },
  { name: 'Coast Region', projects: 28 },
  { name: 'Rift Valley', projects: 32 },
  { name: 'Western Region', projects: 18 },
  { name: 'Nyanza Region', projects: 15 },
  { name: 'Central Region', projects: 14 }
])
</script>

<style scoped>
.hover\:shadow-4:hover {
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.15);
}
</style>