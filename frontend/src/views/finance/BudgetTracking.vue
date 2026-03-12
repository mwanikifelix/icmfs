









<!-- ============================================ -->
<!-- FILE 2: BudgetTracking.vue                  -->
<!-- src/views/finance/BudgetTracking.vue        -->
<!-- ============================================ -->
<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <div class="flex justify-content-between align-items-center mb-4">
          <h5 class="m-0">Budget Tracking</h5>
          <Button label="Export Report" icon="pi pi-download" severity="secondary" />
        </div>

        <!-- Filter Bar -->
        <div class="flex flex-wrap gap-3 mb-4">
          <Select v-model="selectedRegion" :options="regions" placeholder="All Regions" showClear class="w-15rem" />
          <Select v-model="selectedProject" :options="projects" placeholder="All Projects" showClear class="w-15rem" />
          <Select v-model="selectedYear" :options="years" placeholder="Year" class="w-10rem" />
        </div>

        <!-- Budget Table -->
        <DataTable :value="budgets" stripedRows responsiveLayout="scroll">
          <Column field="project" header="Project" sortable />
          <Column field="region" header="Region" sortable />
          <Column field="allocated" header="Allocated Budget">
            <template #body="{ data }">
              KES {{ data.allocated.toLocaleString() }}
            </template>
          </Column>
          <Column field="spent" header="Spent">
            <template #body="{ data }">
              KES {{ data.spent.toLocaleString() }}
            </template>
          </Column>
          <Column field="remaining" header="Remaining">
            <template #body="{ data }">
              <span :class="data.remaining < 0 ? 'text-red-500' : 'text-green-500'">
                KES {{ data.remaining.toLocaleString() }}
              </span>
            </template>
          </Column>
          <Column header="Progress">
            <template #body="{ data }">
              <div class="flex align-items-center gap-2">
                <ProgressBar :value="data.percentUsed" class="flex-1" style="height: 8px" />
                <span class="text-sm">{{ data.percentUsed }}%</span>
              </div>
            </template>
          </Column>
          <Column field="status" header="Status">
            <template #body="{ data }">
              <Tag :value="data.status" :severity="getStatusSeverity(data.status)" />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Button from 'primevue/button'
import Select from 'primevue/select'
import ProgressBar from 'primevue/progressbar'

const selectedRegion = ref(null)
const selectedProject = ref(null)
const selectedYear = ref('2026')

const regions = ref(['Nairobi', 'Coast', 'Rift Valley', 'Western', 'Nyanza', 'Central'])
const projects = ref(['Nairobi Phase 2', 'Mombasa County', 'Kisumu Lakeside', 'Nakuru Heights'])
const years = ref(['2024', '2025', '2026'])

const budgets = ref([
  { project: 'Nairobi Phase 2', region: 'Nairobi', allocated: 450000000, spent: 315000000, remaining: 135000000, percentUsed: 70, status: 'On Track' },
  { project: 'Mombasa County', region: 'Coast', allocated: 320000000, spent: 272000000, remaining: 48000000, percentUsed: 85, status: 'Over Budget' },
  { project: 'Kisumu Lakeside', region: 'Nyanza', allocated: 280000000, spent: 140000000, remaining: 140000000, percentUsed: 50, status: 'On Track' },
  { project: 'Nakuru Heights', region: 'Rift Valley', allocated: 200000000, spent: 80000000, remaining: 120000000, percentUsed: 40, status: 'On Track' },
  { project: 'Eldoret Green', region: 'Rift Valley', allocated: 180000000, spent: 90000000, remaining: 90000000, percentUsed: 50, status: 'On Track' },
])

const getStatusSeverity = (status) => {
  const map = { 'On Track': 'success', 'Over Budget': 'danger', 'At Risk': 'warning' }
  return map[status] || 'info'
}
</script>
