<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">

        <!-- ================= HEADER ================= -->
        <div class="flex justify-content-between align-items-center mb-4">
          <h5>Counties</h5>
        </div>

        <!-- ================= COUNTIES TABLE ================= -->
        <DataTable
          :value="countyRows"
          :paginator="true"
          :rows="10"
          responsiveLayout="scroll"
        >
          <!-- County -->
          <Column field="name" header="County" />

          <!-- Region -->
          <Column field="region" header="Region" />

          <!-- Projects -->
          <Column header="Projects">
            <template #body="{ data }">
              {{ data.projectCount }}
            </template>
          </Column>

          <!-- Active Projects -->
          <Column header="Active">
            <template #body="{ data }">
              <Badge :value="data.active" severity="success" />
            </template>
          </Column>

          <!-- On Hold -->
          <Column header="On Hold">
            <template #body="{ data }">
              <Badge :value="data.onHold" severity="warning" />
            </template>
          </Column>

          <!-- Completed -->
          <Column header="Completed">
            <template #body="{ data }">
              <Badge :value="data.completed" severity="secondary" />
            </template>
          </Column>

          <!-- Actions -->
          <Column header="Actions">
            <template #body="{ data }">
              <Button
                icon="pi pi-eye"
                text
                rounded
                @click="goToProjects(data.name)"
              />
            </template>
          </Column>
        </DataTable>

      </div>
    </div>
  </div>
</template>
<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

/* PrimeVue */
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Badge from "primevue/badge";

/* Data */
import { counties } from "../../components/data/projects.master.js";

const router = useRouter();

/* -----------------------------------
   Build county rows from master data
----------------------------------- */
const countyRows = computed(() => {
  return counties.map(c => {
    const active = c.projects.filter(p => p.status === "in_progress").length;
    const onHold = c.projects.filter(p => p.status === "on_hold").length;
    const completed = c.projects.filter(p => p.status === "completed").length;

    return {
      county_id: c.county_id,
      name: c.name,
      region: c.region,
      projectCount: c.projects.length,
      active,
      onHold,
      completed
    };
  });
});

/* -----------------------------------
   Navigation
----------------------------------- */
const goToProjects = (countyName) => {
  router.push({
    path: "/app/projects",
    query: { county: countyName }
  });
};
</script>
