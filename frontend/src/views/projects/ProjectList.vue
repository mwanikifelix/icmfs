
<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">

        <!-- Header -->
        <div class="flex justify-content-between align-items-center mb-4">
          <h5>Projects</h5>
          <Button
            label="New Project"
            icon="pi pi-plus"
            @click="$router.push('/app/projects/create')"
          />
        </div>

        <!-- Filters -->
        <div class="flex gap-3 mb-3" style="flex-wrap: nowrap;">
          <Dropdown
            v-model="filters.county"
            :options="countyOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Select County"
            showClear
            style="width: 25%;"
          />

          <Dropdown
            v-model="filters.status"
            :options="statusOptions"
            placeholder="Status"
            showClear
            style="width: 25%;"
          />

          <Dropdown
            v-model="filters.sector"
            :options="sectorOptions"
            placeholder="Sector"
            showClear
            style="width: 25%;"
          />

          <Dropdown
            v-model="filters.owner"
            :options="ownerOptions"
            placeholder="Owner Type"
            showClear
            style="width: 25%;"
          />
        </div>

        <!-- Projects Table -->
        <DataTable
          :value="filteredProjects"
          :paginator="true"
          :rows="10"
          responsiveLayout="scroll"
        >
          <Column field="title" header="Project Name" />
          <Column field="county" header="County" />
          <Column field="owner_type" header="Owner" />

          <Column header="Status">
            <template #body="{ data }">
              <Badge
                :value="formatStatus(data.status)"
                :severity="getStatusSeverity(data.status)"
              />
            </template>
          </Column>

          <Column header="Progress">
            <template #body="{ data }">
              <ProgressBar
                :value="data.progress"
                :showValue="false"
                style="height: 6px"
              />
              <small class="block mt-1">{{ data.progress }}%</small>
            </template>
          </Column>

          <Column header="Budget">
            <template #body="{ data }">
              KES {{ data.budget_kes.toLocaleString() }}
            </template>
          </Column>

          <Column header="Actions">
            <template #body="{ data }">
              <Button
                icon="pi pi-eye"
                text
                rounded
                @click="$router.push(`/app/projects/${data.project_id}`)"
              />
              <Button
                icon="pi pi-pencil"
                text
                rounded
                severity="secondary"
                @click="$router.push(`/app/projects/${data.project_id}/edit`)"
              />
            </template>
          </Column>
        </DataTable>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

/* Master data */
import { counties } from "../../components/data/projects.master.js";

/* PrimeVue components */
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Badge from "primevue/badge";
import ProgressBar from "primevue/progressbar";
import Dropdown from "primevue/dropdown";

/* -------------------------------------------------
   Flatten county → projects
-------------------------------------------------- */
const projects = computed(() =>
  counties.flatMap(county =>
    county.projects.map(project => ({
      ...project,
      county: county.name
    }))
  )
);

/* -------------------------------------------------
   Filters state
-------------------------------------------------- */
const filters = ref({
  county: null,
  status: null,
  sector: null,
  owner: null
});

/* -------------------------------------------------
   Filtered projects
-------------------------------------------------- */
const filteredProjects = computed(() => {
  return projects.value.filter(p => {
    return (
      (!filters.value.county || p.county === filters.value.county) &&
      (!filters.value.status || p.status === filters.value.status) &&
      (!filters.value.sector || p.sector === filters.value.sector) &&
      (!filters.value.owner || p.owner_type === filters.value.owner)
    );
  });
});

/* -------------------------------------------------
   Dropdown options
-------------------------------------------------- */
const countyOptions = counties.map(c => ({
  label: c.name,
  value: c.name
}));

const statusOptions = [
  "planned",
  "pending",
  "in_progress",
  "on_hold",
  "completed",
  "cancelled"
];

const sectorOptions = [
  "Housing",
  "Infrastructure",
  "Health",
  "Education"
];

const ownerOptions = [
  "Government",
  "Private",
  "NGO"
];

/* -------------------------------------------------
   Helpers
-------------------------------------------------- */
const getStatusSeverity = status => {
  const map = {
    planned: "info",
    pending: "warning",
    in_progress: "success",
    on_hold: "warning",
    completed: "secondary",
    cancelled: "danger"
  };
  return map[status] || "info";
};

const formatStatus = status => {
  const map = {
    planned: "Planned",
    pending: "Pending",
    in_progress: "In Progress / Ongoing",
    on_hold: "On Hold",
    completed: "Completed",
    cancelled: "Cancelled"
  };
  return map[status] || status;
};
</script>
