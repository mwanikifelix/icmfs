<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">

        <!-- ================= HEADER ================= -->
        <div class="flex justify-content-between align-items-center mb-4">
          <h5>Sub-Counties</h5>
        </div>

        <!-- ================= SUB-COUNTIES TABLE ================= -->
        <DataTable
          :value="subCountyRows"
          :paginator="true"
          :rows="10"
          responsiveLayout="scroll"
        >
          <!-- Sub-County -->
          <Column field="sub_county" header="Sub-County" />

          <!-- County -->
          <Column field="county" header="County" />

          <!-- Region -->
          <Column field="region" header="Region" />

          <!-- Projects -->
          <Column header="Projects">
            <template #body="{ data }">
              {{ data.projectCount }}
            </template>
          </Column>

          <!-- Active -->
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
                @click="goToProjects(data)"
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
   Build sub-county rows
----------------------------------- */
const subCountyRows = computed(() => {
  const map = {};

  counties.forEach(county => {
    county.projects.forEach(project => {
      const sub = project.site?.sub_county;
      if (!sub) return;

      const key = `${county.name}-${sub}`;

      if (!map[key]) {
        map[key] = {
          sub_county: sub,
          county: county.name,
          region: county.region,
          projects: []
        };
      }

      map[key].projects.push(project);
    });
  });

  return Object.values(map).map(row => {
    const active = row.projects.filter(p => p.status === "in_progress").length;
    const onHold = row.projects.filter(p => p.status === "on_hold").length;
    const completed = row.projects.filter(p => p.status === "completed").length;

    return {
      sub_county: row.sub_county,
      county: row.county,
      region: row.region,
      projectCount: row.projects.length,
      active,
      onHold,
      completed
    };
  });
});

/* -----------------------------------
   Navigation
----------------------------------- */
const goToProjects = ({ county, sub_county }) => {
  router.push({
    path: "/app/projects",
    query: {
      county,
      sub_county
    }
  });
};
</script>
