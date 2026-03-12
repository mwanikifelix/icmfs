<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">

        <!-- ================= HEADER ================= -->
        <div class="flex justify-content-between align-items-center mb-4">
          <h5>Regions</h5>
        </div>

        <!-- ================= REGIONS TABLE ================= -->
        <DataTable
          :value="regions"
          :paginator="true"
          :rows="10"
          responsiveLayout="scroll"
        >
          <!-- Region -->
          <Column field="name" header="Region" />

          <!-- Counties -->
          <Column header="Counties">
            <template #body="{ data }">
              {{ data.countyCount }}
            </template>
          </Column>

          <!-- Projects -->
          <Column header="Projects">
            <template #body="{ data }">
              {{ data.projectCount }}
            </template>
          </Column>

          <!-- Status Summary -->
          <Column header="Active Projects">
            <template #body="{ data }">
              <Badge
                :value="data.activeProjects"
                severity="success"
              />
            </template>
          </Column>

          <Column header="On Hold">
            <template #body="{ data }">
              <Badge
                :value="data.onHoldProjects"
                severity="warning"
              />
            </template>
          </Column>

          <!-- Actions -->
          <Column header="Actions">
            <template #body="{ data }">
              <Button
                icon="pi pi-eye"
                text
                rounded
                @click="goToRegion(data.region_id)"
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
   Build regions from counties (SAFE)
----------------------------------- */
const regions = computed(() => {
  const map = {};

  counties.forEach(county => {
    if (!map[county.region]) {
      map[county.region] = {
        region_id: county.region.toLowerCase().replace(/\s+/g, "-"),
        name: county.region,
        counties: [],
        projects: []
      };
    }

    map[county.region].counties.push(county);
    map[county.region].projects.push(...county.projects);
  });

  return Object.values(map).map(region => {
    const active = region.projects.filter(
      p => p.status === "in_progress"
    ).length;

    const onHold = region.projects.filter(
      p => p.status === "on_hold"
    ).length;

    return {
      region_id: region.region_id,
      name: region.name,
      countyCount: region.counties.length,
      projectCount: region.projects.length,
      activeProjects: active,
      onHoldProjects: onHold
    };
  });
});

/* -----------------------------------
   Navigation
----------------------------------- */
const goToRegion = (regionId) => {
  router.push(`/app/regions/${regionId}`);
};
</script>

<style scoped>
/* Optional: subtle spacing polish */
.card h5 {
  font-weight: 600;
}
</style>
