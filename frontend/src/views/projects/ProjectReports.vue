<template>
  <div class="card">

    <h4 class="mb-3">Project Reports</h4>

    <!-- ================= NO REPORTS ================= -->
    <div v-if="!reports.length" class="text-gray-500">
      No reports have been submitted for this project yet.
    </div>

    <!-- ================= REPORT LIST ================= -->
    <DataTable
      v-else
      :value="reports"
      responsiveLayout="scroll"
      stripedRows
    >
      <Column field="report_date" header="Date" />

      <Column field="report_type" header="Type" />

      <Column header="Submitted By">
        <template #body="{ data }">
          {{ data.submitted_by.name }} <br />
          <small class="text-gray-500">{{ data.submitted_by.role }}</small>
        </template>
      </Column>

      <Column header="Progress">
        <template #body="{ data }">
          {{ data.progress_percentage }}%
        </template>
      </Column>

      <Column header="Status Update">
        <template #body="{ data }">
          <span class="line-clamp-2">
            {{ data.status_update }}
          </span>
        </template>
      </Column>

      <Column header="Actions">
        <template #body="{ data }">
          <Button
            icon="pi pi-eye"
            text
            rounded
            @click="viewReport(data)"
          />
          <Button
            icon="pi pi-file-pdf"
            text
            rounded
            severity="secondary"
            @click="exportPdf(data)"
          />
        </template>
      </Column>
    </DataTable>

    <!-- ================= REPORT DETAIL DIALOG ================= -->
    <Dialog
      v-model:visible="showDialog"
      header="Report Details"
      modal
      style="width: 600px"
    >
      <template v-if="selectedReport">

        <p class="mb-3">
          <strong>Date:</strong> {{ selectedReport.report_date }} <br />
          <strong>Type:</strong> {{ selectedReport.report_type }}
        </p>

        <p class="mb-3">
          <strong>Status Update:</strong><br />
          {{ selectedReport.status_update }}
        </p>

        <p class="mb-3">
          <strong>Progress:</strong>
          {{ selectedReport.progress_percentage }}%
        </p>

        <p class="mb-3">
          <strong>Workforce:</strong><br />
          Skilled: {{ selectedReport.workforce.skilled }} <br />
          Unskilled: {{ selectedReport.workforce.unskilled }} <br />
          Supervisors: {{ selectedReport.workforce.supervisors }} <br />
          <strong>Total:</strong> {{ selectedReport.workforce.total }}
        </p>

        <div v-if="selectedReport.issues.length">
          <strong>Issues / Risks</strong>
          <ul class="pl-4 mt-2">
            <li v-for="issue in selectedReport.issues" :key="issue">
              {{ issue }}
            </li>
          </ul>
        </div>

      </template>
    </Dialog>

  </div>
</template>


<script setup>
import { ref, computed } from "vue";
import { useRoute } from "vue-router";

/* PrimeVue */
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Dialog from "primevue/dialog";

/* Data */
import { getProjectActivityById } from "../../components/data/project.site.activity.js";

const route = useRoute();

/* -----------------------------------
   Reports for this project
----------------------------------- */
const reports = computed(() => {
  const activity = getProjectActivityById(route.params.id);
  return activity?.reports || [];
});

/* -----------------------------------
   Dialog logic
----------------------------------- */
const showDialog = ref(false);
const selectedReport = ref(null);

const viewReport = (report) => {
  selectedReport.value = report;
  showDialog.value = true;
};

const exportPdf = (report) => {
  console.log("EXPORT REPORT TO PDF:", report);

  // 🔔 Future:
  // - generate PDF
  // - download
};
</script>
