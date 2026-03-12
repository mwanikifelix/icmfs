<template>
  <div class="bank-payments">
    <div class="page-header">
      <div>
        <span class="page-tag">PAYMENTS · BANK TRANSFERS</span>
        <h1>Bank Payments</h1>
        <p class="page-sub">EFT, RTGS and cheque payments to contractors and suppliers</p>
      </div>
      <button class="btn-primary" @click="showForm = true">+ New Bank Transfer</button>
    </div>

    <div class="kpi-row">
      <div class="kpi" v-for="k in kpis" :key="k.label" :class="k.cls">
        <div class="kpi-val">{{ k.val }}</div>
        <div class="kpi-label">{{ k.label }}</div>
      </div>
    </div>

    <div class="filters-bar">
      <div class="search-wrap">
        <span>🔍</span>
        <input v-model="search" type="text" placeholder="Search beneficiary or reference..." class="search-input" />
      </div>
      <select v-model="filterType" class="filter-select">
        <option value="">All Types</option>
        <option value="eft">EFT</option>
        <option value="rtgs">RTGS</option>
        <option value="cheque">Cheque</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="processed">Processed</option>
        <option value="pending">Pending</option>
        <option value="rejected">Rejected</option>
      </select>
    </div>

    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Ref</th>
            <th>Beneficiary</th>
            <th>Bank / Account</th>
            <th>Type</th>
            <th>Amount (KES)</th>
            <th>Purpose</th>
            <th>Site</th>
            <th>Initiated By</th>
            <th>Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filteredPayments" :key="p.id" class="table-row">
            <td class="mono ref">{{ p.ref }}</td>
            <td>
              <div class="bene-name">{{ p.beneficiary }}</div>
              <div class="bene-kra mono">KRA: {{ p.kra }}</div>
            </td>
            <td>
              <div class="bank-name">{{ p.bank }}</div>
              <div class="acc-no mono">{{ p.account }}</div>
            </td>
            <td><span class="type-badge" :class="p.type">{{ p.type.toUpperCase() }}</span></td>
            <td class="amount">{{ p.amount.toLocaleString() }}</td>
            <td class="purpose">{{ p.purpose }}</td>
            <td class="site-cell">{{ p.site }}</td>
            <td class="initiated">{{ p.initiatedBy }}</td>
            <td class="mono date-cell">{{ p.date }}</td>
            <td><span class="status-badge" :class="p.status">{{ p.status }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- New Transfer Modal -->
    <div class="modal-overlay" v-if="showForm" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>🏦 New Bank Transfer</h2>
          <button class="close-btn" @click="showForm = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Beneficiary Name *</label>
              <input v-model="form.beneficiary" type="text" placeholder="Company or individual name" />
            </div>
            <div class="form-group">
              <label>KRA PIN</label>
              <input v-model="form.kra" type="text" placeholder="A0XXXXXXXXX" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Bank Name *</label>
              <select v-model="form.bank">
                <option value="">Select bank...</option>
                <option>KCB Bank</option>
                <option>Equity Bank</option>
                <option>Co-operative Bank</option>
                <option>NCBA Bank</option>
                <option>Stanbic Bank</option>
                <option>Standard Chartered</option>
                <option>Absa Bank Kenya</option>
              </select>
            </div>
            <div class="form-group">
              <label>Account Number *</label>
              <input v-model="form.account" type="text" placeholder="Account number" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Transfer Type *</label>
              <select v-model="form.type">
                <option value="">Select type...</option>
                <option value="eft">EFT (1-3 business days)</option>
                <option value="rtgs">RTGS (Same day)</option>
                <option value="cheque">Cheque</option>
              </select>
            </div>
            <div class="form-group">
              <label>Amount (KES) *</label>
              <input v-model="form.amount" type="number" placeholder="0.00" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Purpose *</label>
              <select v-model="form.purpose">
                <option>Contractor Payment</option>
                <option>Supplier Invoice</option>
                <option>Consultant Fee</option>
                <option>Equipment Purchase</option>
                <option>Land Acquisition</option>
              </select>
            </div>
            <div class="form-group">
              <label>Site</label>
              <select v-model="form.site">
                <option v-for="s in siteOptions" :key="s">{{ s }}</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-ghost" @click="showForm = false">Cancel</button>
          <button class="btn-primary" @click="submitPayment">Submit Transfer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const showForm = ref(false)
const search = ref('')
const filterType = ref('')
const filterStatus = ref('')
const siteOptions = ['Nairobi Housing — Phase 1', 'Mombasa Infrastructure', 'Kisumu Commercial', 'Nakuru Road Project']
const form = ref({ beneficiary: '', kra: '', bank: '', account: '', type: '', amount: '', purpose: '', site: '' })

const payments = ref([
  { id: 1, ref: 'BNK-001', beneficiary: 'Steel Fabricators Ltd', kra: 'A001234567B', bank: 'KCB Bank', account: '1234567890', type: 'rtgs', amount: 320000, purpose: 'Contractor Payment', site: 'Nairobi Housing', initiatedBy: 'Alice Wanjiku', date: '2025-02-17', status: 'processed' },
  { id: 2, ref: 'BNK-002', beneficiary: 'Arch. Daniel Oduya & Partners', kra: 'A009876543C', bank: 'Equity Bank', account: '0987654321', type: 'eft', amount: 250000, purpose: 'Consultant Fee', site: 'Mombasa Infrastructure', initiatedBy: 'Peter Kamau', date: '2025-02-15', status: 'processed' },
  { id: 3, ref: 'BNK-003', beneficiary: 'Kisumu Aggregate Suppliers', kra: 'A005544332D', bank: 'Co-operative Bank', account: '5544332211', type: 'eft', amount: 180000, purpose: 'Supplier Invoice', site: 'Kisumu Commercial', initiatedBy: 'James Mutua', date: '2025-02-14', status: 'pending' },
  { id: 4, ref: 'BNK-004', beneficiary: 'Nakuru Plant Hire Ltd', kra: 'A007788990E', bank: 'NCBA Bank', account: '7788990011', type: 'cheque', amount: 95000, purpose: 'Equipment Purchase', site: 'Nakuru Road Project', initiatedBy: 'Grace Otieno', date: '2025-02-12', status: 'pending' },
  { id: 5, ref: 'BNK-005', beneficiary: 'Mombasa Concrete Works', kra: 'A003322110F', bank: 'Stanbic Bank', account: '3322110099', type: 'rtgs', amount: 560000, purpose: 'Contractor Payment', site: 'Mombasa Infrastructure', initiatedBy: 'Alice Wanjiku', date: '2025-02-10', status: 'rejected' },
])

const kpis = computed(() => [
  { label: 'Total Transferred', val: 'KES ' + payments.value.filter(p => p.status === 'processed').reduce((a, b) => a + b.amount, 0).toLocaleString(), cls: 'blue' },
  { label: 'Pending', val: payments.value.filter(p => p.status === 'pending').length, cls: 'warn' },
  { label: 'Rejected', val: payments.value.filter(p => p.status === 'rejected').length, cls: 'danger' },
  { label: 'Total Records', val: payments.value.length, cls: 'info' },
])

const filteredPayments = computed(() => payments.value.filter(p =>
  (!search.value || p.beneficiary.toLowerCase().includes(search.value.toLowerCase()) || p.ref.includes(search.value))
  && (!filterType.value || p.type === filterType.value)
  && (!filterStatus.value || p.status === filterStatus.value)
))

function submitPayment() {
  payments.value.unshift({ id: payments.value.length + 1, ref: `BNK-00${payments.value.length + 1}`, ...form.value, amount: Number(form.value.amount), initiatedBy: 'Current User', date: new Date().toISOString().split('T')[0], status: 'pending', kra: form.value.kra || 'N/A' })
  showForm.value = false
  form.value = { beneficiary: '', kra: '', bank: '', account: '', type: '', amount: '', purpose: '', site: '' }
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

*{box-sizing:border-box;margin:0;padding:0}

/* MAIN PAGE */
.bank-payments{
font-family:'Syne',sans-serif;
background:#045dca; /* deep logo blue */
color:#ffffff;
min-height:100vh;
padding:28px 32px;
}

/* HEADER */
.page-header{
display:flex;
justify-content:space-between;
align-items:flex-start;
margin-bottom:24px
}

.page-tag{
font-family:'DM Mono',monospace;
font-size:10px;
letter-spacing:2px;
color:#facc15; /* gold from logo */
text-transform:uppercase;
display:block;
margin-bottom:6px
}

h1{
font-size:28px;
font-weight:800;
color:#ffffff
}

.page-sub{
font-size:13px;
color:#cbd5e1;
margin-top:4px
}

/* BUTTON */
.btn-primary{
background:#16a34a; /* logo green */
color:#fff;
border:none;
padding:10px 20px;
border-radius:8px;
font-weight:700;
font-size:13px;
cursor:pointer
}

.btn-primary:hover{
background:#15803d
}

.btn-ghost{
background:none;
border:1px solid #facc15;
color:#facc15;
padding:10px 20px;
border-radius:8px;
font-size:13px;
cursor:pointer
}

/* KPI */
.kpi-row{display:flex;gap:12px;margin-bottom:20px}

.kpi{
background:#0f3f79;
border-radius:10px;
padding:14px 20px;
flex:1
}

.kpi.blue{border-left:4px solid #3b82f6}
.kpi.warn{border-left:4px solid #facc15}
.kpi.danger{border-left:4px solid #ef4444}
.kpi.info{border-left:4px solid #22c55e}

.kpi-val{
font-size:22px;
font-weight:800;
color:#ffffff
}

.kpi-label{
font-size:11px;
color:#cbd5e1;
text-transform:uppercase;
margin-top:4px
}

/* FILTERS */
.filters-bar{
display:flex;
gap:10px;
margin-bottom:16px
}

.search-wrap{
flex:1;
display:flex;
align-items:center;
gap:8px;
background:#0f3f79;
border-radius:7px;
padding:0 12px
}

.search-input{
flex:1;
background:none;
border:none;
color:#fff;
padding:9px 0;
font-size:13px;
outline:none
}

.filter-select{
background:#0f3f79;
color:#fff;
padding:9px 12px;
border-radius:7px;
border:none;
font-size:13px
}

/* TABLE */
.table-wrap{
background:#ffffff;
border-radius:12px;
overflow-x:auto
}

.data-table{
width:100%;
border-collapse:collapse
}

.data-table thead th{
padding:12px 14px;
text-align:left;
font-size:14px;
font-family:'DM Mono',monospace;
letter-spacing:1px;
color:#334155;
border-bottom:1px solid #e2e8f0;
text-transform:uppercase
}

.table-row{
border-bottom:1px solid #e2e8f0
}

.table-row:hover{
background:#f1f5f9
}

.table-row td{
padding:16px 18px;
vertical-align:middle;
color:#1e293b
}

.ref{
font-size:11px;
color:#2563eb
}

.bene-name{
font-size:12px;
font-weight:600
}

.bene-kra{
font-size:10px;
color:#64748b
}

.bank-name{
font-size:12px;
font-weight:600
}

.acc-no{
font-size:10px;
color:#64748b
}

/* TYPE BADGES */

.type-badge{
font-family:'DM Mono',monospace;
font-size:9px;
padding:3px 7px;
border-radius:4px;
font-weight:600
}

.type-badge.eft{
background:#e0f2fe;
color:#0369a1
}

.type-badge.rtgs{
background:#ede9fe;
color:#6d28d9
}

.type-badge.cheque{
background:#fef3c7;
color:#b45309
}

/* STATUS */

.status-badge{
font-family:'DM Mono',monospace;
font-size:9px;
padding:4px 8px;
border-radius:4px;
text-transform:uppercase
}

.status-badge.processed{
background:#dcfce7;
color:#15803d
}

.status-badge.pending{
background:#fef3c7;
color:#b45309
}

.status-badge.rejected{
background:#fee2e2;
color:#991b1b
}

/* MODAL */

.modal-overlay{
position:fixed;
inset:0;
background:rgba(0,0,0,0.5);
z-index:100;
display:flex;
align-items:center;
justify-content:center
}

.modal{
background:#ffffff;
border-radius:16px;
width:640px;
max-height:90vh;
overflow-y:auto
}

.modal-header{
display:flex;
justify-content:space-between;
align-items:center;
padding:20px 28px;
border-bottom:1px solid #e2e8f0
}

.modal-header h2{
font-size:17px;
font-weight:700;
color:#0b2e59
}

.close-btn{
background:none;
border:none;
color:#64748b;
font-size:18px;
cursor:pointer
}

.modal-body{
padding:24px 28px;
display:flex;
flex-direction:column;
gap:14px
}

.modal-footer{
display:flex;
justify-content:flex-end;
gap:10px;
padding:16px 28px;
border-top:1px solid #e2e8f0
}

/* FORM */

.form-row{
display:grid;
grid-template-columns:1fr 1fr;
gap:14px
}

.form-group{
display:flex;
flex-direction:column;
gap:6px
}

.form-group label{
font-size:11px;
color:#475569;
text-transform:uppercase;
letter-spacing:0.5px;
font-family:'DM Mono',monospace
}

.form-group input,
.form-group select{
background:#f8fafc;
border:1px solid #cbd5e1;
color:#1e293b;
padding:10px 12px;
border-radius:7px;
font-size:13px
}

.form-group input:focus,
.form-group select:focus{
outline:none;
border-color:#2563eb
}
</style>