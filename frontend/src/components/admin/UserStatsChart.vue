<template>
  <Bar :data="chartData" />
</template>

<script setup>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale);

defineProps({
  stats: Object,
});

const chartData = computed(() => ({
  labels: ["Total", "Active", "Staff", "Admins"],
  datasets: [
    {
      label: "Users",
      data: [
        props.stats.total,
        props.stats.active,
        props.stats.staff,
        props.stats.admins,
      ],
      backgroundColor: "#3b82f6",
    },
  ],
}));
</script>
