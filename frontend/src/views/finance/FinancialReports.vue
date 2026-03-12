
<!-- ============================================ -->
<!-- FILE 4: FinancialReports.vue                -->
<!-- src/views/finance/FinancialReports.vue      -->
<!-- ============================================ -->
<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <div class="flex justify-content-between align-items-center mb-4">
          <h5 class="m-0">Financial Reports</h5>
          <Button label="Generate Report" icon="pi pi-file-pdf" />
        </div>

        <!-- Report Type Tabs -->
        <TabView>
          <!-- Summary Report -->
          <TabPanel header="Summary Report">
            <div class="grid mt-3">
              <div class="col-12 md:col-3">
                <div class="surface-100 p-3 border-round text-center">
                  <p class="text-500 text-sm">Total Projects</p>
                  <p class="text-900 text-2xl font-bold">45</p>
                </div>
              </div>
              <div class="col-12 md:col-3">
                <div class="surface-100 p-3 border-round text-center">
                  <p class="text-500 text-sm">Total Budget</p>
                  <p class="text-900 text-2xl font-bold">KES 2.45B</p>
                </div>
              </div>
              <div class="col-12 md:col-3">
                <div class="surface-100 p-3 border-round text-center">
                  <p class="text-500 text-sm">Total Spent</p>
                  <p class="text-900 text-2xl font-bold">KES 1.65B</p>
                </div>
              </div>
              <div class="col-12 md:col-3">
                <div class="surface-100 p-3 border-round text-center">
                  <p class="text-500 text-sm">Budget Utilization</p>
                  <p class="text-900 text-2xl font-bold">67%</p>
                </div>
              </div>
              <div class="col-12 mt-3">
                <Chart type="line" :data="lineChartData" :options="chartOptions" />
              </div>
            </div>
          </TabPanel>

          <!-- By Region -->
          <TabPanel header="By Region">
            <DataTable :value="regionReports" stripedRows class="mt-3">
              <Column field="region" header="Region" />
              <Column field="projects" header="Projects" />
              <Column field="budget" header="Budget">
                <template #body="{ data }">KES {{ data.budget.toLocaleString() }}</template>
              </Column>
              <Column field="spent" header="Spent">
                <template #body="{ data }">KES {{ data.spent.toLocaleString() }}</template>
              </Column>
              <Column field="utilization" header="Utilization">
                <template #body="{ data }">
                  <ProgressBar :value="data.utilization" style="height: 8px" />
                </template>
              </Column>
            </DataTable>
          </TabPanel>

          <!-- Expense Report -->
          <TabPanel header="Expense Breakdown">
            <div class="grid mt-3">
              <div class="col-12 md:col-6">
                <Chart type="pie" :data="expenseChartData" />
              </div>
              <div class="col-12 md:col-6">
                <DataTable :value="expenseBreakdown" stripedRows>
                  <Column field="category" header="Category" />
                  <Column field="amount" header="Amount">
                    <template #body="{ data }">KES {{ data.amount.toLocaleString() }}</template>
                  </Column>
                  <Column field="percentage" header="%" />
                </DataTable>
              </div>
            </div>
          </TabPanel>
        </TabView>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Chart from 'primevue/chart'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import ProgressBar from 'primevue/progressbar'

const lineChartData = ref({
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    { label: 'Budget', data: [400, 410, 420, 430, 440, 450], borderColor: '#3B82F6', fill: false },
    { label: 'Spent', data: [200, 280, 350, 410, 500, 580], borderColor: '#EF4444', fill: false }
  ]
})

const expenseChartData = ref({
  labels: ['Materials', 'Labour', 'Equipment', 'Consultancy', 'Transport', 'Overhead'],
  datasets: [{
    data: [40, 25, 15, 10, 5, 5],
    backgroundColor: ['#3B82F6','#10B981','#F59E0B','#EF4444','#8B5CF6','#EC4899']
  }]
})

const chartOptions = ref({ responsive: true, maintainAspectRatio: false })

const regionReports = ref([
  { region: 'Nairobi', projects: 12, budget: 850000000, spent: 595000000, utilization: 70 },
  { region: 'Coast', projects: 8, budget: 620000000, spent: 527000000, utilization: 85 },
  { region: 'Rift Valley', projects: 10, budget: 520000000, spent: 260000000, utilization: 50 },
  { region: 'Western', projects: 6, budget: 280000000, spent: 140000000, utilization: 50 },
  { region: 'Nyanza', projects: 5, budget: 230000000, spent: 92000000, utilization: 40 },
  { region: 'Central', projects: 4, budget: 180000000, spent: 36000000, utilization: 20 },
])

const expenseBreakdown = ref([
  { category: 'Materials', amount: 660000000, percentage: '40%' },
  { category: 'Labour', amount: 412500000, percentage: '25%' },
  { category: 'Equipment', amount: 247500000, percentage: '15%' },
  { category: 'Consultancy', amount: 165000000, percentage: '10%' },
  { category: 'Transport', amount: 82500000, percentage: '5%' },
  { category: 'Overhead', amount: 82500000, percentage: '5%' },
])
</script>