<template>
  <div class="card">
    <h4 class="mb-4">Project Timeline</h4>

    <Timeline :value="timeline" align="alternate">

      <!-- TIMELINE MARKER -->
      <template #marker="{ item }">
        <span
          class="timeline-marker"
          :class="item.status"
        >
          <i :class="item.icon"></i>
        </span>
      </template>

      <!-- TIMELINE CONTENT -->
      <template #content="{ item }">
        <div class="timeline-card">
          <div class="flex justify-content-between mb-2">
            <span class="font-semibold">{{ item.title }}</span>
            <Tag
              :value="item.statusLabel"
              :severity="item.tagSeverity"
            />
          </div>

          <p class="text-sm mb-2">
            {{ item.description }}
          </p>

          <div class="text-xs text-gray-500 flex gap-3">
            <span>
              <i class="pi pi-calendar mr-1"></i>
              {{ item.date }}
            </span>

            <span v-if="item.progress !== null">
              <i class="pi pi-chart-line mr-1"></i>
              {{ item.progress }}%
            </span>
          </div>
        </div>
      </template>

    </Timeline>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Timeline from "primevue/timeline";
import Tag from "primevue/tag";

const timeline = ref([
  {
    title: "Project Initiation",
    description: "Project officially approved and site mobilization started.",
    date: "2023-05-01",
    progress: 0,
    status: "completed",
    statusLabel: "Completed",
    tagSeverity: "success",
    icon: "pi pi-flag"
  },
  {
    title: "Foundation Works",
    description: "Excavation and foundation concrete works completed.",
    date: "2024-02-18",
    progress: 30,
    status: "completed",
    statusLabel: "Completed",
    tagSeverity: "success",
    icon: "pi pi-check-circle"
  },
  {
    title: "Structural Works",
    description: "Columns, beams, and slab construction ongoing.",
    date: "2025-01-10",
    progress: 68,
    status: "in-progress",
    statusLabel: "In Progress",
    tagSeverity: "warning",
    icon: "pi pi-spinner"
  },
  {
    title: "Finishing & Handover",
    description: "Internal finishes, inspection, and handover.",
    date: "Expected: 2026-02",
    progress: null,
    status: "upcoming",
    statusLabel: "Upcoming",
    tagSeverity: "info",
    icon: "pi pi-clock"
  }
]);
</script>
