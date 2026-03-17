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
          :loading="loading"
          :paginator="true"
          :rows="10"
          responsiveLayout="scroll"
        >

          <Column field="name" header="County" />

          <Column field="region" header="Region" />

          <Column header="Projects">
            <template #body="{ data }">
              {{ data.projectCount }}
            </template>
          </Column>

          <Column header="Planned">
            <template #body="{ data }">
              <Badge :value="data.planned" severity="info" />
            </template>
          </Column>

          <Column header="Active">
            <template #body="{ data }">
              <Badge :value="data.active" severity="success" />
            </template>
          </Column>

          <Column header="In Progress">
            <template #body="{ data }">
              <Badge :value="data.inProgress" severity="primary" />
            </template>
          </Column>

          <Column header="On Hold">
            <template #body="{ data }">
              <Badge :value="data.onHold" severity="warning" />
            </template>
          </Column>

          <Column header="Completed">
            <template #body="{ data }">
              <Badge :value="data.completed" severity="secondary" />
            </template>
          </Column>

          <Column header="At Risk">
            <template #body="{ data }">
              <Badge :value="data.atRisk" severity="danger" />
            </template>
          </Column>

          <Column header="Cancelled">
            <template #body="{ data }">
              <Badge :value="data.cancelled" severity="danger" />
            </template>
          </Column>

          <!-- Actions -->
          <Column header="Actions">
            <template #body="{ data }">

              <!-- View projects -->
              <Button
                icon="pi pi-eye"
                text
                rounded
                @click="goToProjects(data.county_id)"
              />

              <!-- Edit project -->
              <Button
                icon="pi pi-pencil"
                text
                rounded
                severity="info"
                @click="editCounty(data.county_id)"
              />

            </template>
          </Column>

        </DataTable>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/api";

/* PrimeVue */
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Badge from "primevue/badge";

const router = useRouter();

const counties = ref([]);
const projects = ref([]);
const loading = ref(false);

/* -------------------------
   Load counties + projects
------------------------- */
async function loadData() {
  loading.value = true;

  try {
    const [countyRes, projectRes] = await Promise.all([
      api.get("/api/projects/counties/"),
      api.get("/api/projects/projects/")
    ]);

    counties.value = Array.isArray(countyRes.data)
      ? countyRes.data
      : countyRes.data.results ?? [];

    projects.value = Array.isArray(projectRes.data)
      ? projectRes.data
      : projectRes.data.results ?? [];

  } catch (err) {
    console.error("Failed to load data", err);
  } finally {
    loading.value = false;
  }
}

/* -------------------------
   Build county rows
------------------------- */
const countyRows = computed(() => {

  return counties.value
    .map(c => {

      const countyProjects = projects.value.filter(
        p => p.county === c.id
      );

      const planned = countyProjects.filter(
        p => p.status === "planned"
      ).length;

      const active = countyProjects.filter(
        p => p.status === "active"
      ).length;

      const inProgress = countyProjects.filter(
        p => p.status === "in_progress"
      ).length;

      const onHold = countyProjects.filter(
        p => p.status === "on_hold"
      ).length;

      const completed = countyProjects.filter(
        p => p.status === "completed"
      ).length;

      const atRisk = countyProjects.filter(
        p => p.status === "at_risk"
      ).length;

      const cancelled = countyProjects.filter(
        p => p.status === "cancelled"
      ).length;

      return {
        county_id: c.id,
        name: c.name,
        region: c.region_detail?.name || "—",
        projectCount: countyProjects.length,
        planned,
        active,
        inProgress,
        onHold,
        completed,
        atRisk,
        cancelled
      };
    })

    /* Only counties with projects */
    .filter(c => c.projectCount > 0);
});

/* -------------------------
   Navigation
------------------------- */

const goToProjects = (countyId) => {
  router.push({
    path: "/app/projects",
    query: { county: countyId }
  });
};

const editCounty = (countyId) => {
  router.push(`/app/projects/${countyId}/edit`);
};

/* -------------------------
   Load on start
------------------------- */

onMounted(loadData);
</script>

<style scoped>
.card h5 {
  font-weight: 600;
}
</style>