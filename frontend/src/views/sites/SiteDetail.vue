<script setup>
import { useRoute } from "vue-router";
import { sites } from "@/components/data/sites";

const route = useRoute();
const site = sites.find(s => s.id === Number(route.params.id));
</script>

<template>
  <div class="card">
    <h2>{{ site.name }}</h2>
    <p>Status: {{ site.status }}</p>
    <p>Workers: {{ site.workers }}</p>

    <TabView>
      <TabPanel header="Workforce">
        <WorkforceManagement />
      </TabPanel>
      <TabPanel header="Daily Reports">
        <DailyReports />
      </TabPanel>
    </TabView>
  </div>
</template>
