
<!-- ============================================ -->
<!-- FILE 5: Payments.vue                        -->
<!-- src/views/finance/Payments.vue              -->
<!-- ============================================ -->
<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <div class="flex justify-content-between align-items-center mb-4">
          <h5 class="m-0">Payments</h5>
          <div class="flex gap-2">
            <Button label="New Payment" icon="pi pi-plus" @click="paymentDialog = true" />
            <Button label="Export" icon="pi pi-download" severity="secondary" />
          </div>
        </div>

        <!-- Stats -->
        <div class="grid mb-4">
          <div class="col-12 md:col-3">
            <div class="surface-100 p-3 border-round text-center">
              <p class="text-500 text-sm mb-1">Total Payments</p>
              <p class="text-900 text-xl font-bold">KES 1.2B</p>
            </div>
          </div>
          <div class="col-12 md:col-3">
            <div class="surface-100 p-3 border-round text-center">
              <p class="text-500 text-sm mb-1">M-Pesa Payments</p>
              <p class="text-green-600 text-xl font-bold">KES 450M</p>
            </div>
          </div>
          <div class="col-12 md:col-3">
            <div class="surface-100 p-3 border-round text-center">
              <p class="text-500 text-sm mb-1">Bank Transfers</p>
              <p class="text-blue-600 text-xl font-bold">KES 750M</p>
            </div>
          </div>
          <div class="col-12 md:col-3">
            <div class="surface-100 p-3 border-round text-center">
              <p class="text-500 text-sm mb-1">Pending</p>
              <p class="text-yellow-600 text-xl font-bold">KES 85M</p>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="flex flex-wrap gap-3 mb-4">
          <Select v-model="selectedType" :options="['M-Pesa', 'Bank Transfer', 'Cheque']" placeholder="Payment Type" showClear class="w-12rem" />
          <Select v-model="selectedStatus" :options="['Completed', 'Pending', 'Failed']" placeholder="Status" showClear class="w-10rem" />
          <InputText v-model="searchQuery" placeholder="Search recipient..." class="w-14rem" />
        </div>

        <!-- Payments Table -->
        <DataTable :value="filteredPayments" stripedRows responsiveLayout="scroll" :paginator="true" :rows="10">
          <Column field="date" header="Date" sortable />
          <Column field="recipient" header="Recipient" />
          <Column field="project" header="Project" />
          <Column field="type" header="Type">
            <template #body="{ data }">
              <Tag :value="data.type" :severity="data.type === 'M-Pesa' ? 'success' : 'info'" />
            </template>
          </Column>
          <Column field="reference" header="Reference" />
          <Column field="amount" header="Amount" sortable>
            <template #body="{ data }">
              KES {{ data.amount.toLocaleString() }}
            </template>
          </Column>
          <Column field="status" header="Status">
            <template #body="{ data }">
              <Tag :value="data.status" :severity="getStatusSeverity(data.status)" />
            </template>
          </Column>
          <Column header="Actions">
            <template #body="{ data }">
              <Button icon="pi pi-eye" text rounded severity="info" @click="viewPayment(data)" />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>

    <!-- New Payment Dialog -->
    <Dialog v-model:visible="paymentDialog" header="New Payment" modal class="p-fluid" style="width: 480px">
      <div class="formgrid grid">
        <div class="field col-12">
          <label>Recipient *</label>
          <InputText v-model="newPayment.recipient" placeholder="Enter recipient name" />
        </div>
        <div class="field col-12 md:col-6">
          <label>Amount (KES) *</label>
          <InputNumber v-model="newPayment.amount" mode="currency" currency="KES" locale="en-KE" />
        </div>
        <div class="field col-12 md:col-6">
          <label>Payment Type *</label>
          <Select v-model="newPayment.type" :options="['M-Pesa', 'Bank Transfer', 'Cheque']" placeholder="Select Type" />
        </div>
        <div class="field col-12" v-if="newPayment.type === 'M-Pesa'">
          <label>Phone Number *</label>
          <InputText v-model="newPayment.phone" placeholder="e.g. 0712345678" />
        </div>
        <div class="field col-12">
          <label>Project</label>
          <Select v-model="newPayment.project" :options="['Nairobi Phase 2', 'Mombasa County', 'Kisumu Lakeside']" placeholder="Select Project" />
        </div>
        <div class="field col-12">
          <label>Notes</label>
          <Textarea v-model="newPayment.notes" rows="3" placeholder="Payment notes..." />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" severity="secondary" @click="paymentDialog = false" />
        <Button label="Process Payment" icon="pi pi-send" @click="processPayment" />
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
import Textarea from 'primevue/textarea'
import Dialog from 'primevue/dialog'

const selectedType = ref(null)
const selectedStatus = ref(null)
const searchQuery = ref('')
const paymentDialog = ref(false)

const newPayment = ref({ recipient: '', amount: 0, type: '', phone: '', project: '', notes: '' })

const payments = ref([
  { date: '2026-02-01', recipient: 'ABC Contractors', project: 'Nairobi Phase 2', type: 'M-Pesa', reference: 'MPE123456', amount: 2500000, status: 'Completed' },
  { date: '2026-02-01', recipient: 'XYZ Suppliers', project: 'Mombasa County', type: 'Bank Transfer', reference: 'BNK789012', amount: 1800000, status: 'Completed' },
  { date: '2026-02-02', recipient: 'DEF Materials', project: 'Kisumu Lakeside', type: 'M-Pesa', reference: 'MPE345678', amount: 950000, status: 'Pending' },
  { date: '2026-02-02', recipient: 'GHI Consultants', project: 'Nakuru Heights', type: 'Bank Transfer', reference: 'BNK901234', amount: 500000, status: 'Pending' },
  { date: '2026-02-03', recipient: 'JKL Services', project: 'Nairobi Phase 2', type: 'M-Pesa', reference: 'MPE567890', amount: 750000, status: 'Failed' },
])

const filteredPayments = computed(() => {
  return payments.value.filter(p => {
    const matchType = !selectedType.value || p.type === selectedType.value
    const matchStatus = !selectedStatus.value || p.status === selectedStatus.value
    const matchSearch = !searchQuery.value || p.recipient.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchType && matchStatus && matchSearch
  })
})

const getStatusSeverity = (status) => {
  const map = { Completed: 'success', Pending: 'warning', Failed: 'danger' }
  return map[status] || 'info'
}

const viewPayment = (data) => { console.log('View payment:', data) }

const processPayment = () => {
  payments.value.push({ ...newPayment.value, date: new Date().toISOString().split('T')[0], reference: 'REF' + Date.now(), status: 'Pending' })
  paymentDialog.value = false
  newPayment.value = { recipient: '', amount: 0, type: '', phone: '', project: '', notes: '' }
}
</script>