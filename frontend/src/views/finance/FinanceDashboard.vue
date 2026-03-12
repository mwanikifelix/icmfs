<!-- ============================================ -->
<!-- FILE 1: FinanceDashboard.vue                -->
<!-- src/views/finance/FinanceDashboard.vue      -->
<!-- ============================================ -->
<template>
  <div class="grid">

    <!-- Stats Cards -->
    <div class="col-12 md:col-6 xl:col-3">
      <div class="card mb-0">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Total Budget</span>
            <div class="text-900 font-medium text-xl">KES 2.45B</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width:2.5rem;height:2.5rem">
            <i class="pi pi-dollar text-blue-500 text-xl"></i>
          </div>
        </div>
        <span class="text-green-500 font-medium">%4.2 </span>
        <span class="text-500">from last quarter</span>
      </div>
    </div>

    <div class="col-12 md:col-6 xl:col-3">
      <div class="card mb-0">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Total Spent</span>
            <div class="text-900 font-medium text-xl">KES 1.65B</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-orange-100 border-round" style="width:2.5rem;height:2.5rem">
            <i class="pi pi-chart-bar text-orange-500 text-xl"></i>
          </div>
        </div>
        <span class="text-orange-500 font-medium">67% </span>
        <span class="text-500">of total budget</span>
      </div>
    </div>

    <div class="col-12 md:col-6 xl:col-3">
      <div class="card mb-0">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Pending Payments</span>
            <div class="text-900 font-medium text-xl">KES 450M</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-yellow-100 border-round" style="width:2.5rem;height:2.5rem">
            <i class="pi pi-clock text-yellow-500 text-xl"></i>
          </div>
        </div>
        <span class="text-yellow-500 font-medium">12 </span>
        <span class="text-500">pending approvals</span>
      </div>
    </div>

    <div class="col-12 md:col-6 xl:col-3">
      <div class="card mb-0">
        <div class="flex justify-content-between mb-3">
          <div>
            <span class="block text-500 font-medium mb-3">Available Funds</span>
            <div class="text-900 font-medium text-xl">KES 350M</div>
          </div>
          <div class="flex align-items-center justify-content-center bg-green-100 border-round" style="width:2.5rem;height:2.5rem">
            <i class="pi pi-wallet text-green-500 text-xl"></i>
          </div>
        </div>
        <span class="text-green-500 font-medium">14.3% </span>
        <span class="text-500">of total budget</span>
      </div>
    </div>

    <!-- Monthly Expenses Chart -->
    <div class="col-12 xl:col-6">
      <div class="card">
        <h5>Monthly Expenses</h5>
        <Chart type="bar" :data="monthlyChartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Budget Distribution Chart -->
    <div class="col-12 xl:col-6">
      <div class="card">
        <h5>Budget Distribution by Region</h5>
        <Chart type="doughnut" :data="regionChartData" :options="doughnutOptions" />
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="col-12">
      <div class="card">
        <div class="flex justify-content-between align-items-center mb-3">
          <h5 class="m-0">Recent Transactions</h5>
          <router-link to="/app/finance/expenses">
            <Button label="View All" text />
          </router-link>
        </div>
        <DataTable :value="transactions" stripedRows responsiveLayout="scroll">
          <Column field="date" header="Date" />
          <Column field="description" header="Description" />
          <Column field="project" header="Project" />
          <Column field="amount" header="Amount">
            <template #body="{ data }">
              <span>KES {{ data.amount.toLocaleString() }}</span>
            </template>
          </Column>
          <Column field="category" header="Category" />
          <Column field="status" header="Status">
            <template #body="{ data }">
              <Tag :value="data.status" :severity="data.status === 'Approved' ? 'success' : 'warning'" />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import Chart from 'primevue/chart'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Button from 'primevue/button'

const monthlyChartData = ref({
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [{
    label: 'Expenses (Million KES)',
    backgroundColor: '#3B82F6',
    data: [180, 220, 195, 240, 210, 260]
  }]
})

const regionChartData = ref({
  labels: ['Nairobi', 'Coast', 'Rift Valley', 'Western', 'Nyanza', 'Central'],
  datasets: [{
    data: [45, 28, 32, 18, 15, 14],
    backgroundColor: ['#3B82F6','#10B981','#F59E0B','#EF4444','#8B5CF6','#EC4899']
  }]
})

const chartOptions = ref({ responsive: true, maintainAspectRatio: false })
const doughnutOptions = ref({ responsive: true, maintainAspectRatio: false })

const transactions = ref([
  { date: '2026-02-01', description: 'Cement Supply', project: 'Nairobi Phase 2', amount: 320000, category: 'Materials', status: 'Approved' },
  { date: '2026-02-01', description: 'Steel Reinforcement', project: 'Mombasa County', amount: 780000, category: 'Materials', status: 'Approved' },
  { date: '2026-02-02', description: 'Labour Payment', project: 'Kisumu Lakeside', amount: 450000, category: 'Labour', status: 'Pending' },
  { date: '2026-02-02', description: 'Equipment Hire', project: 'Nakuru Heights', amount: 250000, category: 'Equipment', status: 'Pending' },
  { date: '2026-02-03', description: 'Architect Fees', project: 'Eldoret Green', amount: 150000, category: 'Consultancy', status: 'Approved' },
])
</script>
