
<!-- ============================================ -->
<!-- FILE 3: Expenses.vue                        -->
<!-- src/views/finance/Expenses.vue              -->
<!-- ============================================ -->
<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <div class="flex justify-content-between align-items-center mb-4">
          <h5 class="m-0">Expenses</h5>
          <div class="flex gap-2">
            <Button label="Add Expense" icon="pi pi-plus" @click="openExpenseDialog" />
            <Button label="Export" icon="pi pi-download" severity="secondary" />
          </div>
        </div>

        <!-- Filters -->
        <div class="flex flex-wrap gap-3 mb-4">
          <DatePicker v-model="dateRange" selectionMode="range" placeholder="Date Range" showIcon class="w-15rem" />
          <Select v-model="selectedCategory" :options="categories" placeholder="All Categories" showClear class="w-12rem" />
          <Select v-model="selectedStatus" :options="['Approved', 'Pending', 'Rejected']" placeholder="All Statuses" showClear class="w-12rem" />
          <InputText v-model="searchQuery" placeholder="Search..." class="w-12rem" />
        </div>

        <DataTable :value="filteredExpenses" stripedRows responsiveLayout="scroll" :paginator="true" :rows="10">
          <Column field="date" header="Date" sortable />
          <Column field="description" header="Description" />
          <Column field="project" header="Project" />
          <Column field="category" header="Category">
            <template #body="{ data }">
              <Tag :value="data.category" severity="info" />
            </template>
          </Column>
          <Column field="amount" header="Amount" sortable>
            <template #body="{ data }">
              KES {{ data.amount.toLocaleString() }}
            </template>
          </Column>
          <Column field="submittedBy" header="Submitted By" />
          <Column field="status" header="Status">
            <template #body="{ data }">
              <Tag :value="data.status" :severity="getSeverity(data.status)" />
            </template>
          </Column>
          <Column header="Actions">
            <template #body="{ data }">
              <div class="flex gap-1">
                <Button icon="pi pi-eye" text rounded severity="info" @click="viewExpense(data)" />
                <Button icon="pi pi-pencil" text rounded severity="warning" @click="editExpense(data)" />
                <Button v-if="data.status === 'Pending'" icon="pi pi-check" text rounded severity="success" @click="approveExpense(data)" />
              </div>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>

    <!-- Add Expense Dialog -->
    <Dialog v-model:visible="expenseDialog" header="Add Expense" modal class="p-fluid" style="width: 500px">
      <div class="formgrid grid">
        <div class="field col-12">
          <label>Description *</label>
          <InputText v-model="newExpense.description" placeholder="Enter description" />
        </div>
        <div class="field col-12 md:col-6">
          <label>Amount (KES) *</label>
          <InputNumber v-model="newExpense.amount" mode="currency" currency="KES" locale="en-KE" />
        </div>
        <div class="field col-12 md:col-6">
          <label>Category *</label>
          <Select v-model="newExpense.category" :options="categories" placeholder="Select Category" />
        </div>
        <div class="field col-12 md:col-6">
          <label>Date *</label>
          <DatePicker v-model="newExpense.date" dateFormat="yy-mm-dd" showIcon />
        </div>
        <div class="field col-12 md:col-6">
          <label>Project</label>
          <Select v-model="newExpense.project" :options="projects" placeholder="Select Project" />
        </div>
        <div class="field col-12">
          <label>Receipt (Optional)</label>
          <FileUpload mode="basic" accept="image/*,.pdf" :maxFileSize="5000000" chooseLabel="Upload Receipt" />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" severity="secondary" @click="expenseDialog = false" />
        <Button label="Submit Expense" @click="submitExpense" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Button from 'primevue/button'
import Select from 'primevue/select'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import DatePicker from 'primevue/datepicker'
import Dialog from 'primevue/dialog'
import FileUpload from 'primevue/fileupload'

const dateRange = ref(null)
const selectedCategory = ref(null)
const selectedStatus = ref(null)
const searchQuery = ref('')
const expenseDialog = ref(false)

const categories = ref(['Materials', 'Labour', 'Equipment', 'Consultancy', 'Transport', 'Overhead'])
const projects = ref(['Nairobi Phase 2', 'Mombasa County', 'Kisumu Lakeside', 'Nakuru Heights'])

const newExpense = ref({ description: '', amount: 0, category: '', date: null, project: '' })

const expenses = ref([
  { date: '2026-02-01', description: 'Cement Supply', project: 'Nairobi Phase 2', category: 'Materials', amount: 320000, submittedBy: 'John Doe', status: 'Approved' },
  { date: '2026-02-01', description: 'Steel Reinforcement', project: 'Mombasa County', category: 'Materials', amount: 780000, submittedBy: 'Jane Smith', status: 'Approved' },
  { date: '2026-02-02', description: 'Labour Payment', project: 'Kisumu Lakeside', category: 'Labour', amount: 450000, submittedBy: 'Hassan Ali', status: 'Pending' },
  { date: '2026-02-02', description: 'Equipment Hire', project: 'Nakuru Heights', category: 'Equipment', amount: 250000, submittedBy: 'Mary Wanja', status: 'Pending' },
  { date: '2026-02-03', description: 'Architect Fees', project: 'Nairobi Phase 2', category: 'Consultancy', amount: 150000, submittedBy: 'Peter Kamau', status: 'Rejected' },
])

const filteredExpenses = computed(() => {
  return expenses.value.filter(e => {
    const matchCategory = !selectedCategory.value || e.category === selectedCategory.value
    const matchStatus = !selectedStatus.value || e.status === selectedStatus.value
    const matchSearch = !searchQuery.value || e.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchCategory && matchStatus && matchSearch
  })
})

const getSeverity = (status) => {
  const map = { Approved: 'success', Pending: 'warning', Rejected: 'danger' }
  return map[status] || 'info'
}

const openExpenseDialog = () => { expenseDialog.value = true }
const viewExpense = (data) => { console.log('View:', data) }
const editExpense = (data) => { console.log('Edit:', data) }
const approveExpense = (data) => { data.status = 'Approved' }
const submitExpense = () => {
  expenses.value.push({ ...newExpense.value, submittedBy: 'Current User', status: 'Pending' })
  expenseDialog.value = false
  newExpense.value = { description: '', amount: 0, category: '', date: null, project: '' }
}
</script>