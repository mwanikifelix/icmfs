<template>
  <section class="py-6 bg-primary">
    <div class="max-w-screen-xl mx-auto px-4">
      <div class="grid text-center">
        <div 
          v-for="stat in statsData" 
          :key="stat.label" 
          class="col-12 md:col-3"
        >
          <div class="text-white mb-2">
            <i :class="stat.icon" class="text-5xl mb-3"></i>
            <div class="text-4xl font-bold">{{ stat.value }}</div>
            <div class="text-xl">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const stats = ref({
  projects: 152,
  regions: 8,
  units: 50,
  users: 1200
})

const statsData = computed(() => [
  {
    icon: 'pi pi-building',
    value: `${stats.value.projects}+`,
    label: 'Active Projects'
  },
  {
    icon: 'pi pi-map',
    value: stats.value.regions,
    label: 'Regions Covered'
  },
  {
    icon: 'pi pi-home',
    value: `${stats.value.units}K+`,
    label: 'Housing Units'
  },
  {
    icon: 'pi pi-users',
    value: `${stats.value.users}+`,
    label: 'Active Users'
  }
])
</script>