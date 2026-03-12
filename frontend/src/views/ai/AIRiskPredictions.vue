<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <h5>AI Risk Predictions</h5>
        <DataTable :value="risks">
          <Column field="risk" header="Risk"></Column>
          <Column field="probability" header="Probability">
            <template #body="slotProps">
              <ProgressBar :value="slotProps.data.probability" :showValue="false" />
              <span class="text-sm">{{ slotProps.data.probability }}%</span>
            </template>
          </Column>
          <Column field="impact" header="Impact">
            <template #body="slotProps">
              <Badge :value="slotProps.data.impact" :severity="getImpactSeverity(slotProps.data.impact)" />
            </template>
          </Column>
          <Column field="mitigation" header="Mitigation"></Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ProgressBar from 'primevue/progressbar';
import Badge from 'primevue/badge';

const risks = ref([
  { risk: 'Weather delays', probability: 65, impact: 'High', mitigation: 'Schedule buffer added' },
  { risk: 'Material shortage', probability: 30, impact: 'Medium', mitigation: 'Backup suppliers identified' }
]);

const getImpactSeverity = (impact) => {
  const map = { High: 'danger', Medium: 'warn', Low: 'info' };
  return map[impact];
};
</script>