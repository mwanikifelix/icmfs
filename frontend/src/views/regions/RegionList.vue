<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">

        <!-- HEADER -->
        <div class="flex justify-content-between align-items-center mb-4">
          <h5>Regions</h5>
        </div>

        <!-- REGIONS TABLE -->
        <DataTable
          :value="regions"
          :loading="loading"
          :paginator="true"
          :rows="10"
          responsiveLayout="scroll"
        >

          <Column field="name" header="Region" />

          <Column header="Counties">
            <template #body="{ data }">
              {{ data.countyCount }}
            </template>
          </Column>

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

              <!-- View projects in region -->
              <Button
                icon="pi pi-eye"
                text
                rounded
                @click="goToRegion(data.region_id)"
              />

              <!-- Edit project -->
              <Button
                icon="pi pi-pencil"
                text
                rounded
                severity="info"
                @click="editRegion(data.region_id)"
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

const projects = ref([]);
const loading = ref(false);

/* -------------------------
   Load projects
------------------------- */
async function loadProjects() {
  loading.value = true;

  try {
    const res = await api.get("/api/projects/projects/");

    projects.value = Array.isArray(res.data)
      ? res.data
      : (res.data.results ?? []);

  } catch (err) {
    console.error("Failed to load projects", err);
  } finally {
    loading.value = false;
  }
}

/* -------------------------
   Group projects by region
------------------------- */
const regions = computed(() => {

  const map = {};

  projects.value.forEach(project => {

    const regionName = project.region_detail?.name || "Unknown";

    if (!map[regionName]) {
      map[regionName] = {
        region_id: project.region,
        name: regionName,
        counties: new Set(),
        projects: []
      };
    }

    map[regionName].projects.push(project);

    if (project.county_detail?.name) {
      map[regionName].counties.add(project.county_detail.name);
    }

  });

  return Object.values(map).map(region => {

    const planned = region.projects.filter(
      p => p.status === "planned"
    ).length;

    const active = region.projects.filter(
      p => p.status === "active"
    ).length;

    const inProgress = region.projects.filter(
      p => p.status === "in_progress"
    ).length;

    const onHold = region.projects.filter(
      p => p.status === "on_hold"
    ).length;

    const completed = region.projects.filter(
      p => p.status === "completed"
    ).length;

    const atRisk = region.projects.filter(
      p => p.status === "at_risk"
    ).length;

    const cancelled = region.projects.filter(
      p => p.status === "cancelled"
    ).length;

    return {
      region_id: region.region_id,
      name: region.name,
      countyCount: region.counties.size,
      projectCount: region.projects.length,
      planned,
      active,
      inProgress,
      onHold,
      completed,
      atRisk,
      cancelled
    };
  });

});

/* -------------------------
   Navigation
------------------------- */

const goToRegion = (regionId) => {
  router.push({
    path: "/app/projects",
    query: { region: regionId }
  });
};

const editRegion = (regionId) => {
  router.push(`/app/projects/${regionId}/edit`);
};

onMounted(loadProjects);
</script>

<style scoped>
.card h5 {
  font-weight: 600;
}
</style>