<template>
  <div class="card">

    <h4 class="mb-3">Project Risks & AI Predictions</h4>

    <!-- ================= NO RISKS ================= -->
    <div v-if="!risks.length" class="text-gray-500">
      No risks have been identified for this project yet.
    </div>

    <!-- ================= RISK TABLE ================= -->
    <DataTable
      v-else
      :value="risks"
      responsiveLayout="scroll"
      stripedRows
    >
      <Column field="category" header="Category" />

      <Column header="Risk Description">
        <template #body="{ data }">
          {{ data.description }}
        </template>
      </Column>

      <Column header="Probability">
        <template #body="{ data }">
          {{ data.probability }}%
        </template>
      </Column>

      <Column header="Impact">
        <template #body="{ data }">
          {{ data.impact }}
        </template>
      </Column>

      <Column header="Severity">
        <template #body="{ data }">
          <Tag
            :value="data.severity"
            :severity="severityColor(data.severity)"
          />
        </template>
      </Column>

      <Column header="AI Confidence">
        <template #body="{ data }">
          {{ data.confidence_score }}%
        </template>
      </Column>

      <Column header="Source">
        <template #body="{ data }">
          <Tag
            :value="data.source"
            :severity="data.source === 'AI' ? 'info' : 'secondary'"
          />
        </template>
      </Column>

      <Column header="Actions">
        <template #body="{ data }">
          <Button
            icon="pi pi-eye"
            text
            rounded
            @click="viewRisk(data)"
          />
        </template>
      </Column>
    </DataTable>

    <!-- ================= RISK DETAIL ================= -->
    <Dialog
      v-model:visible="showDialog"
      header="Risk Analysis"
      modal
      style="width: 600px"
    >
      <template v-if="selectedRisk">

        <p class="mb-2">
          <strong>Category:</strong> {{ selectedRisk.category }}
        </p>

        <p class="mb-2">
          <strong>Description:</strong><br />
          {{ selectedRisk.description }}
        </p>

        <p class="mb-2">
          <strong>Probability:</strong> {{ selectedRisk.probability }}%
        </p>

        <p class="mb-2">
          <strong>Impact:</strong> {{ selectedRisk.impact }}
        </p>

        <p class="mb-2">
          <strong>Severity:</strong> {{ selectedRisk.severity }}
        </p>

        <p class="mb-2">
          <strong>Mitigation Strategy:</strong><br />
          {{ selectedRisk.mitigation }}
        </p>

        <p class="text-sm text-gray-500 mt-3">
          Predicted on {{ selectedRisk.predicted_on }} |
          Confidence: {{ selectedRisk.confidence_score }}%
        </p>

      </template>
    </Dialog>

  </div>
</template>
<script setup>
import { ref } from "vue";

/* PrimeVue */
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import Tag from "primevue/tag";

/* -----------------------------------
   DUMMY AI RISK DATA (replace later)
----------------------------------- */
const risks = ref([
  {
    risk_id: "RISK-001",
    category: "Weather",
    description: "Heavy rainfall may delay foundation and excavation works.",
    probability: 65,
    impact: "Schedule Delay",
    severity: "High",
    confidence_score: 82,
    mitigation: "Adjust work schedule and deploy drainage pumps.",
    predicted_on: "2026-02-01",
    source: "AI"
  },
  {
    risk_id: "RISK-002",
    category: "Supply Chain",
    description: "Possible cement shortages due to supplier backlog.",
    probability: 48,
    impact: "Cost Increase",
    severity: "Medium",
    confidence_score: 74,
    mitigation: "Engage alternative suppliers and increase buffer stock.",
    predicted_on: "2026-02-01",
    source: "AI"
  },
  {
    risk_id: "RISK-003",
    category: "Safety",
    description: "High workforce density increases accident risk.",
    probability: 30,
    impact: "Safety Incident",
    severity: "Low",
    confidence_score: 68,
    mitigation: "Increase safety supervision and PPE enforcement.",
    predicted_on: "2026-01-28",
    source: "Manual"
  }
]);

/* -----------------------------------
   Dialog logic
----------------------------------- */
const showDialog = ref(false);
const selectedRisk = ref(null);

const viewRisk = (risk) => {
  selectedRisk.value = risk;
  showDialog.value = true;
};

/* -----------------------------------
   Severity coloring
----------------------------------- */
const severityColor = (severity) => {
  return {
    Low: "success",
    Medium: "warning",
    High: "danger"
  }[severity] || "info";
};
</script>
